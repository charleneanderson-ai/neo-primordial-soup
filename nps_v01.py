from dataclasses import dataclass, field
from typing import List, Tuple


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


agents = [
    Agent(name="Agent_1", position=(1, 1)),
    Agent(name="Agent_2", position=(5, 5)),
    Agent(name="Agent_3", position=(8, 2)),
]


for agent in agents:
    print(agent.describe())


for turn in range(0, 10):
    print(f"\n--- Turn {turn} ---")

    for agent in agents:
        if agent.position[0] < 9:
            agent.position = (
                agent.position[0] + 1,
                agent.position[1]
            )
        print(agent.describe())