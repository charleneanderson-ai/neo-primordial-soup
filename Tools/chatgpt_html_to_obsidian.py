#!/usr/bin/env python3
"""
Convert a ChatGPT data-export chat.html file into one Markdown file per conversation.

Usage:
    python chatgpt_html_to_obsidian.py "C:\path\to\chat.html"

Optional:
    python chatgpt_html_to_obsidian.py "C:\path\to\chat.html" --output "C:\path\to\Markdown Chats"
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("America/Chicago")


def extract_json_data(html: str):
    start_marker = "var jsonData = "
    end_marker = "\n      var assetsJson"

    start = html.find(start_marker)
    if start == -1:
        raise ValueError("Could not find 'var jsonData' in chat.html.")

    start += len(start_marker)
    end = html.find(end_marker, start)
    if end == -1:
        raise ValueError("Could not find the end of ChatGPT conversation data.")

    return json.loads(html[start:end].strip())


def safe_filename(name: str, max_len: int = 150) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)
    name = re.sub(r"\s+", " ", name).strip().rstrip(". ")
    if not name:
        name = "Untitled Conversation"
    return name[:max_len].rstrip()


def iso_local(ts):
    if not ts:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(LOCAL_TZ).isoformat(timespec="seconds")


def date_local(ts):
    if not ts:
        return "Unknown-Date"
    return datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(LOCAL_TZ).strftime("%Y.%m.%d")


def yaml_quote(value):
    if value is None:
        return '""'
    return json.dumps(str(value), ensure_ascii=False)


def current_branch(conv):
    """
    Follow parent links backward from current_node, then reverse.
    This preserves the active/final branch instead of dumping abandoned branches.
    """
    mapping = conv.get("mapping") or {}
    node_id = conv.get("current_node")
    ordered = []
    seen = set()

    while node_id and node_id not in seen:
        seen.add(node_id)
        node = mapping.get(node_id)
        if not node:
            break
        ordered.append(node)
        node_id = node.get("parent")

    ordered.reverse()
    return ordered


def part_to_text(part):
    if isinstance(part, str):
        return part

    if not isinstance(part, dict):
        return ""

    # Voice-mode / multimodal transcription
    if part.get("content_type") == "audio_transcription":
        return part.get("text", "")

    # Common text-bearing fields
    for key in ("text", "content", "caption"):
        value = part.get(key)
        if isinstance(value, str):
            return value

    # Preserve a useful marker for image references if present
    if part.get("content_type") in {"image_asset_pointer", "image"}:
        return "[Image attachment]"

    return ""


def message_text(msg):
    content = msg.get("content") or {}
    ctype = content.get("content_type")

    # Do not export hidden/internal reasoning material.
    if ctype in {"thoughts", "reasoning_recap"}:
        return ""

    parts = content.get("parts")
    if isinstance(parts, list):
        chunks = [part_to_text(p) for p in parts]
        return "\n".join(c for c in chunks if c).strip()

    text = content.get("text")
    if isinstance(text, str):
        return text.strip()

    return ""


def render_conversation(conv):
    title = conv.get("title") or "Untitled Conversation"
    created = iso_local(conv.get("create_time"))
    updated = iso_local(conv.get("update_time"))
    conv_id = conv.get("conversation_id") or conv.get("id") or ""
    archived = bool(conv.get("is_archived"))

    lines = [
        "---",
        f"title: {yaml_quote(title)}",
        f"created: {yaml_quote(created)}",
        f"updated: {yaml_quote(updated)}",
        f"conversation_id: {yaml_quote(conv_id)}",
        f"archived: {'true' if archived else 'false'}",
        'source: "ChatGPT export"',
        'tags:',
        '  - chatgpt-export',
        "---",
        "",
        f"# {title}",
        "",
    ]

    count = 0
    for node in current_branch(conv):
        msg = node.get("message")
        if not msg:
            continue

        role = (msg.get("author") or {}).get("role")
        if role not in {"user", "assistant"}:
            continue

        body = message_text(msg)
        if not body:
            continue

        label = "Charlene" if role == "user" else "Assistant"
        msg_time = iso_local(msg.get("create_time"))

        lines.append(f"## {label}")
        if msg_time:
            lines.append(f"*{msg_time}*")
        lines.append("")
        lines.append(body)
        lines.append("")
        count += 1

    return "\n".join(lines).rstrip() + "\n", count


def unique_path(output_dir: Path, base_name: str):
    candidate = output_dir / f"{base_name}.md"
    if not candidate.exists():
        return candidate

    i = 2
    while True:
        candidate = output_dir / f"{base_name} ({i}).md"
        if not candidate.exists():
            return candidate
        i += 1


def convert(input_file: Path, output_dir: Path):
    html = input_file.read_text(encoding="utf-8", errors="replace")
    conversations = extract_json_data(html)

    output_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0

    for conv in conversations:
        markdown, msg_count = render_conversation(conv)
        if msg_count == 0:
            skipped += 1
            continue

        title = conv.get("title") or "Untitled Conversation"
        date_prefix = date_local(conv.get("create_time"))
        base = safe_filename(f"{date_prefix} - {title}")
        out_path = unique_path(output_dir, base)
        out_path.write_text(markdown, encoding="utf-8")
        written += 1

    return len(conversations), written, skipped


def main():
    parser = argparse.ArgumentParser(
        description="Convert ChatGPT chat.html export to Obsidian-friendly Markdown files."
    )
    parser.add_argument("input", type=Path, help="Path to chat.html")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help='Output folder. Default: sibling folder named "Markdown Chats".',
    )
    args = parser.parse_args()

    input_file = args.input.expanduser().resolve()
    if not input_file.exists():
        raise SystemExit(f"File not found: {input_file}")

    output_dir = args.output.expanduser().resolve() if args.output else input_file.parent / "Markdown Chats"

    total, written, skipped = convert(input_file, output_dir)

    print()
    print("Conversion complete.")
    print(f"Conversations found: {total}")
    print(f"Markdown files written: {written}")
    print(f"Skipped (no visible user/assistant text): {skipped}")
    print(f"Output folder: {output_dir}")


if __name__ == "__main__":
    main()
