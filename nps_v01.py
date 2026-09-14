from dataclasses import dataclass, field
from typing import List, Tuple
import random


@dataclass
class Agent:
    name: str
    position: Tuple[int, int]
    energy: int = 10
    age: int = 0
    memory: List[str] = field(default_factory=list)

    def remember(self, event: str):
        self.memory.append(event)

    def describe(self):
        return {
            "name": self.name,
            "position": self.position,
            "energy": self.energy,
            "age": self.age,
            "memory": self.memory,
        }

DIRECTIONS = {
    "east": (1, 0),
    "west": (-1, 0),
    "north": (0, 1),
    "south": (0, -1),
    "stay": (0, 0),
}

agents = [
    Agent(name="Agent_1", position=(9, 1)),
    Agent(name="Agent_2", position=(9, 5)),
    Agent(name="Agent_3", position=(9, 2)),
]


for agent in agents:
    print(agent.describe())


for turn in range(1, 11):
    print(f"\n--- Turn {turn} ---")

    for agent in agents:
        chosen_direction = random.choice(list(DIRECTIONS.keys()))
        movement = DIRECTIONS[chosen_direction]
        dx, dy = movement

        current_x, current_y = agent.position
        new_x = current_x + dx
        new_y = current_y + dy

        move_result = "blocked"

        if chosen_direction == "stay":
            move_result = "stayed"
        elif 0 <= new_x <= 9 and 0 <= new_y <= 9:
            agent.position = (new_x, new_y)
            move_result = "moved"

        print(agent.name, chosen_direction, move_result) 
        print(agent.describe())