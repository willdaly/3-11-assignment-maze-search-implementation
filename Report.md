# 3.11 Assignment: Maze Search Implementation Report

Student Name: Will Daly  
Course: Northeastern AAI6600 Applied AI
Date: 2-21-226

## Introduction to Search Algorithms

Search algorithms are methods for finding a path from an initial state to a goal state in a state space. In maze solving, the state space is the set of all reachable coordinates in the maze, actions are movement directions (up, down, left, right), and the transition model determines the next state after taking an action.

Uninformed (blind) algorithms, such as Breadth-First Search (BFS) and Depth-First Search (DFS), do not use knowledge of how far a state is from the goal. Informed (heuristic) algorithms, such as Greedy Best-First Search, use a heuristic estimate to prioritize which states to explore next.

## Selected Algorithms

This implementation uses three algorithms:

1. **Maze Solver One: Breadth-First Search (BFS)**
	- Type: Blind search
	- Data structure: Queue (`deque`)
	- Behavior: Explores states level by level

2. **Maze Solver Two: Greedy Best-First Search**
	- Type: Heuristic search
	- Data structure: Priority queue (`heapq`)
	- Behavior: Expands the state with the lowest heuristic value first

3. **Maze Solver Three: Depth-First Search (DFS)**
	- Type: Blind search
	- Data structure: Stack (Python list)
	- Behavior: Explores one branch deeply before backtracking

## Heuristics Used

The heuristic search algorithm (`maze_solver_two`) uses **Manhattan distance**:

$$
h(n) = |x_n - x_g| + |y_n - y_g|
$$

Where:
- $(x_n, y_n)$ is the current state
- $(x_g, y_g)$ is the goal state

Rationale: Manhattan distance is appropriate for a grid with four-direction movement and no diagonal actions. It estimates how many horizontal/vertical steps remain to the exit.

## Performance Comparison

I ran all three solvers on the required maze and compared path quality, runtime, and memory usage.

### Test Setup

- Maze size: 10 x 6
- Environment: macOS / Python 3.13.11
- Number of runs per algorithm: 20
- Timing method: `time.perf_counter()`

### Results Table

| Algorithm | Path Found? | Path Length (steps) | Time (ms) | Space Use (qualitative) | Notes |
|---|---:|---:|---:|---|---|
| BFS | Yes | 20 | 0.0668 | High | Optimal path quality; highest memory in this test |
| Greedy Best-First | Yes | 20 | 0.0793 | Low | Matched BFS path length; slowest runtime in this maze |
| DFS | Yes | 20 | 0.0589 | Low | Fastest runtime; explored slightly fewer states than BFS/Greedy |

### Summary

- Fastest algorithm: DFS
- Shortest path: Tie (BFS, Greedy Best-First, DFS)
- Most memory-efficient in this test: Greedy Best-First

### How to interpret the evaluation metrics

The script `evaluate_report_metrics.py` reports four groups of metrics. I interpret them as follows:

- **Time complexity (empirical)**: Use **Avg Time (ms)** to compare practical speed on the same maze. Lower is better.
- **Space complexity (empirical)**: Use **Peak Memory (KiB)** to compare memory use during execution. Lower is better.
- **Solution quality**: Use **Path Length** (number of `*` cells). For the same maze, a shorter path is better; matching BFS generally indicates optimality in this unweighted setting.
- **Search space traversal**: Use **Transition Calls** and **Expanded States~** to estimate how much of the search space was explored before finding the goal. Fewer expansions usually indicate a more efficient search.

For this report, these values provide empirical evidence, while Big-O expressions (for example, $O(V + E)$) describe asymptotic growth behavior.

## Optimality, Time, and Space Analysis

### BFS
- **Optimality**: Finds the shortest path in an unweighted grid.
- **Time complexity**: $O(V + E)$
- **Space complexity**: $O(V)$
- **Observation in this maze**: BFS found a valid optimal-length path (20 steps) with 0.0668 ms average runtime, but used the highest peak memory (5.53 KiB) among the three solvers.

### Greedy Best-First Search
- **Optimality**: Not guaranteed to find the shortest path.
- **Time complexity**: Depends on heuristic guidance and maze structure.
- **Space complexity**: Typically stores many frontier states in priority queue.
- **Observation in this maze**: Greedy Best-First matched BFS path length (20 steps) on this maze, but had the slowest average runtime (0.0793 ms) while remaining memory-efficient (3.95 KiB peak).

### DFS
- **Optimality**: Not guaranteed shortest path.
- **Time complexity**: $O(V + E)$ in graph traversal terms.
- **Space complexity**: Up to $O(V)$ in worst case (depth/path + bookkeeping).
- **Observation in this maze**: DFS was the fastest in this test (0.0589 ms), used low memory (3.98 KiB), and also produced a 20-step path for this specific maze.

## Maze Variations and Performance Impact

Changes to the maze can significantly affect algorithm performance:

1. **More dead ends / long corridors**
	- DFS may spend more time exploring deep wrong branches.
	- BFS remains complete but may use more memory.

2. **Higher wall density**
	- Can reduce branching factor but increase blocked attempts.
	- Heuristic search may still perform well if goal direction remains informative.

3. **Open maze with many possible paths**
	- BFS explores many alternatives at each level (higher memory).
	- Greedy often reaches the goal quickly but can choose suboptimal routes.

4. **Start and goal far apart with obstacles near goal**
	- Greedy may be misled by local heuristic minima.
	- BFS is slower but reliable for shortest path.

### Conditions where each performs best

- **Best for shortest path correctness**: BFS
- **Best for quick approximate path**: Greedy Best-First Search
- **Best when memory is constrained and path optimality is not required**: DFS

## Real-life Application

One real-life situation where these algorithms apply is indoor navigation (for example, routing through a hospital or office building).

- BFS is useful when the shortest path is required (e.g., emergency response route).
- Greedy Best-First can provide fast route suggestions when quick response is preferred.
- DFS can be useful for exhaustive exploration tasks such as checking all reachable rooms in inspection workflows.

## Conclusion

This project demonstrates the tradeoffs between blind and heuristic search. BFS provides strong optimality guarantees for unweighted mazes, Greedy Best-First improves speed using Manhattan distance but may sacrifice optimality, and DFS offers simple deep exploration with different performance characteristics. The best algorithm depends on whether the priority is shortest path, runtime, or memory usage.