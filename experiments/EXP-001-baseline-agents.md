# EXP-001: Baseline Agents

## Purpose

Establish a behavioral baseline for agents operating under purely deterministic rules before introducing memory and interaction.

## Configuration

The current configuration consists of three agents placed within a 10 x 10 Cartesian grid. No agents currently have memory, nor can they interact with each other.

The simulation runs for 10 turns. During each turn, the program iterates through all three agents before advancing to the next turn. 

Agent state currently consists of:
- Agent_1: position=(1, 1)
- Agent_2: position=(5, 5)
- Agent_3: position=(8, 2)

Memory, age, and energy state have not yet been implemented. No movement or interaction rules are currently active. 

Output is observed through console logging during each turn, allowing the state and behavior of each agent to be inspected throughout the simulation. Because no behavior rules are currently active, each turn reports the same agent state.

## Expected Behavior

Each agent should report the same position and state on every turn, with no changes across the 10-turn simulation.

## Observed Behavior

All three agents reported identical state information across all 10 turns. No positions changed, and no agent behavior varied between turns.

## Unexpected Behavior

None observed.

## Questions Raised

What changes become observable once the first movement rule is introduced?

## Next Step

Introduce a single deterministic movement rule and compare agent state changes against this baseline.