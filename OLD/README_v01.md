# Neo-Primordial Soup (NPS)

NPS explores what happens when simple AI agents can persist, interact, inherit information, and alter one another's environment over time.

## At a Glance

**Language:** Python  
**Focus:** Multi-Agent Simulation, Agentic AI, Emergent Behavior, AI Evaluation  
**Current Version:** v0.1  
**Status:** Active Development

NPS is currently establishing its deterministic experimental substrate before adding persistent memory, agent-to-agent interaction, and later LLM-driven cognition.

## v0.1 Objective

Create a closed local environment with three simple agents, persistent memory, and a shared space. Log every interaction and observe whether any behavior emerges that was not explicitly scripted.

## Why v0.1 Is Non-LLM

v0.1 deliberately uses deterministic Python agents rather than language models. The goal is to establish and understand the experimental substrate before introducing LLM-driven cognition.

## Research Question

What happens when simple autonomous agents persist, interact, retain information, and alter a shared environment over time?

## Current State

Neo-Primordial Soup is in early v0.1 development. The current build establishes the basic simulation structure, including multiple agents, agent identity and position, a shared coordinate space, and turn-based execution.

The project is being developed incrementally so that each new capability can be understood, tested, and observed before additional complexity is introduced.

## Current Capabilities

- Multiple persistent agent objects
- Individual agent identity and position
- Cartesian grid-based environment
- Turn-based simulation loop
- Agent position updates
- Console output for observing agent state and behavior

## What I'm Investigating

- How increasingly complex behavior can arise from simple agent rules
- How persistence and memory affect behavior over time
- How agents influence one another through a shared environment
- How environmental changes alter subsequent agent behavior
- How unexpected behavior can be distinguished from behavior implied by the underlying rules
- How multi-agent behavior can be logged and evaluated reproducibly

## Development Approach

NPS is being built through hands-on, AI-assisted development. AI is used as a learning, research, and debugging partner while the underlying Python concepts, architectural decisions, implementation, testing, and observed behavior are examined directly.

The project intentionally grows in small increments rather than beginning with a complex agent framework. This makes it possible to understand how each capability changes the system.

## Roadmap

### v0.1 — Experimental Substrate
- Establish multiple agents
- Create a shared environment
- Implement turn-based behavior
- Add persistent state
- Log agent activity

### Next
- Persistent agent memory
- Agent-to-agent interaction
- Environmental modification
- Structured experiment logging
- Behavioral metrics and evaluation

### Later
- Introduce LLM-driven cognition
- Compare deterministic and LLM-driven agent behavior
- Explore increasingly autonomous agent decision-making
- Develop reproducible evaluation methods for emergent behavior

## Status

Active development — August 2026 
