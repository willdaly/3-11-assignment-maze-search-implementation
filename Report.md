# 3.11 Assignment: Maze Search Implementation Report

Student Name: Will Daly  
Course: Northeastern AAI6600 Applied AI  
Assignment: Module 3.11 Maze Search Implementation  
Date: March 23, 2026

## Introduction to Search Algorithms

Search algorithms are methods for exploring a problem space in order to move from an initial state to a goal state. In a maze, each reachable coordinate can be treated as a state, the legal actions are moves up, down, left, and right, and the goal is to find a valid path from `S` to `E` without crossing walls marked by `X`.

Search methods are commonly divided into two broad categories: uninformed search and informed search. Uninformed, or blind, search algorithms do not use any estimate of how close a state is to the goal. Instead, they follow a general traversal strategy such as exploring by depth or by breadth. Informed, or heuristic, search algorithms use additional knowledge to rank candidate states so that the search is biased toward states that appear closer to the goal.

This assignment is a useful comparison because maze solving highlights the strengths and weaknesses of different search strategies very clearly. Some algorithms are better at guaranteeing the shortest path. Others are faster on specific maze layouts but may return a longer route. Some use more memory because they must store a large frontier, while others use less memory but may spend time exploring the wrong parts of the maze.

## Maze Representation

The program reads mazes in the format described in the assignment brief:

- The first line gives the width and height.
- `S` marks the start location.
- `E` marks the exit.
- `X` marks walls.
- A blank space marks an open cell.
- `*` is written into the returned solution to show the discovered path.

Internally, the maze is stored as a two-dimensional list of characters. A state is represented as a coordinate pair `(row, column)`. The transition model checks whether moving in a direction stays inside the grid and avoids walls.

## Selected Algorithms

This implementation includes three algorithms, satisfying the assignment requirement to use at least one blind search and at least one heuristic search.

### Maze Solver One: Breadth-First Search

Breadth-First Search (BFS) is an uninformed search algorithm. It uses a queue and explores the maze level by level. That means it first examines all states one move away from the start, then all states two moves away, and so on.

Why it matters:

- BFS is complete for this maze representation.
- In an unweighted maze, BFS guarantees the shortest path in number of moves.
- Its main drawback is memory use, because it may have to store many frontier states at the same time.

### Maze Solver Two: Greedy Best-First Search

Greedy Best-First Search is an informed search algorithm. It uses a priority queue and expands the state with the lowest heuristic estimate first. Instead of exploring evenly in all directions, it tries to move toward the goal as quickly as possible.

Why it matters:

- It often finds a solution quickly when the heuristic is informative.
- It can use less search effort on simple mazes.
- It is not guaranteed to return the shortest path.

### Maze Solver Three: Depth-First Search

Depth-First Search (DFS) is another uninformed search algorithm. It uses a stack and explores one branch as deeply as possible before backtracking.

Why it matters:

- DFS is simple to implement.
- It may reach a solution quickly in some maze layouts.
- It does not guarantee the shortest path.
- It can spend a long time in deep dead ends if the maze structure is unfavorable.

## Heuristic Function

The heuristic used by Greedy Best-First Search is Manhattan distance:

$$
h(n) = |x_n - x_g| + |y_n - y_g|
$$

Where:

- $(x_n, y_n)$ is the current state.
- $(x_g, y_g)$ is the goal state.

This heuristic is appropriate because movement is limited to four directions and diagonal moves are not allowed. Manhattan distance estimates how many horizontal and vertical steps remain between the current state and the exit. It does not account for walls, so it can sometimes be overly optimistic, but it is still a useful guide for directing the search toward the goal.

## Experimental Setup

I evaluated the three algorithms using the maze file included in this repository, `maze.txt`, which is a 10 x 6 maze. The scripts `evaluate_solvers.py` and `evaluate_report_metrics.py` were used to gather runtime, memory, and traversal metrics.

Test conditions:

- Maze size: 10 x 6
- Operating system: macOS
- Programming language: Python
- Number of timing runs: 20 per algorithm
- Timing method: `time.perf_counter()`
- Memory measurement: `tracemalloc`

The main point of this experiment is not to prove theoretical complexity, but to compare how the algorithms behave on the same maze under the same conditions.

## Performance Comparison

The following values were produced by the evaluation script at the time this report was prepared.

| Algorithm | Path Found? | Path Length | Avg Time (ms) | Peak Memory (KiB) | Transition Calls | Expanded States Estimate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BFS | Yes | 20 | 0.0468 | 4.66 | 88 | 22.0 |
| Greedy Best-First | Yes | 20 | 0.0567 | 3.94 | 88 | 22.0 |
| DFS | Yes | 20 | 0.0434 | 3.97 | 84 | 21.0 |

### Interpretation of the results

All three algorithms found a valid path through this maze, and all three returned a path with 20 `*` cells. On this specific input, that means they all found paths of equal marked length. BFS is still the strongest choice if shortest-path optimality must be guaranteed, because BFS has that property in an unweighted grid, while Greedy Best-First Search and DFS do not.

DFS had the lowest average runtime in this specific experiment. Greedy Best-First Search was slightly slower than BFS even though it used a heuristic. That result is possible because the maze is small and simple, so the extra priority queue overhead can offset the benefit of heuristic guidance. Greedy search often shows stronger benefits on larger or more open mazes.

Peak memory use was highest for BFS at 4.66 KiB. This matches the usual theoretical expectation because BFS stores a broader frontier while exploring level by level. DFS and Greedy Best-First Search used slightly less memory on this maze.

The transition-call and expanded-state estimates were very close, but DFS explored slightly fewer states than BFS and Greedy Best-First Search in this run. That suggests the search order used by DFS happened to align slightly better with this maze layout. On more complex mazes, these differences would likely become much larger.

## Optimality, Time, and Space Analysis

### Breadth-First Search

- Optimality: Guaranteed to find the shortest path in this unweighted maze.
- Time complexity: $O(V + E)$ for graph traversal.
- Space complexity: $O(V)$ in the worst case.

BFS is the most reliable algorithm when the quality of the solution matters most. In a maze where every move has equal cost, BFS ensures that the first time the goal is reached, the discovered path is the shortest one. The cost of that guarantee is higher memory usage.

### Greedy Best-First Search

- Optimality: Not guaranteed.
- Time complexity: Depends heavily on maze structure and heuristic quality.
- Space complexity: Can still become large because it stores frontier states in a priority queue.

Greedy Best-First Search tries to reach the goal quickly by always moving toward the state that appears closest to the exit. This can be very efficient when the heuristic points in a helpful direction, but it can also make poor decisions when walls force the correct path away from the goal before returning toward it later.

### Depth-First Search

- Optimality: Not guaranteed.
- Time complexity: $O(V + E)$ for full traversal.
- Space complexity: Up to $O(V)$ in the worst case, though often lower than BFS in practice.

DFS is useful when memory is limited or when any valid solution is acceptable. However, it is sensitive to exploration order. If the algorithm follows a bad branch early, it may spend substantial effort before backtracking and finding the exit.

## Maze Changes That Affect Performance

Changes to the maze can noticeably alter the relative performance of the algorithms.

### More dead ends and deep corridors

Long dead-end corridors generally hurt DFS the most because it can spend a lot of time going deep into incorrect branches before backtracking. BFS remains reliable, but it may need to keep many frontier states in memory. Greedy Best-First Search may also perform poorly if the heuristic keeps pulling the search toward blocked regions near the goal.

### More open space

Large open areas increase the number of branching choices. BFS can become expensive in memory because it explores many states at the same distance from the start. Greedy Best-First Search often benefits in these layouts because Manhattan distance can guide the search more directly toward the exit.

### Obstacles near the goal

If the maze places walls close to the exit, Greedy Best-First Search can be misled because the heuristic still rates nearby cells as attractive even when they are on the wrong side of a barrier. BFS handles this more robustly because it explores by distance rather than by heuristic score.

### Narrow single-solution mazes

If the maze is mostly a long, narrow path with little branching, DFS can perform very well because committing deeply to a branch is unlikely to be a mistake. In that kind of structure, BFS gives little practical advantage over DFS.

## Conditions That Favor Each Algorithm

The best algorithm depends on what is being optimized.

- Best choice for shortest-path correctness: BFS
- Best choice for fast approximate guidance on larger open mazes: Greedy Best-First Search
- Best choice when any valid path is acceptable and memory must stay modest: DFS

If I were designing a system where every move has a cost and path quality matters, I would prefer BFS over the other two algorithms used here. If the system instead needed a fast route suggestion and occasional suboptimal paths were acceptable, Greedy Best-First Search would be a reasonable choice. If the goal were simple exploration with minimal implementation overhead, DFS would be the simplest option.

## Real-Life Application

One real-life situation I have encountered is navigating large buildings such as hospitals, schools, and office complexes where rooms are spread across long hallways and it is easy to take a wrong turn.

For example, a hospital navigation system might use a shortest-path strategy to direct staff or visitors to an emergency room, medicine cabinet, or operating suite as efficiently as possible. In that case, BFS is a good conceptual fit because shortest travel distance matters. A heuristic-driven method such as Greedy Best-First Search could be useful when a very quick route suggestion is needed and the environment is large. DFS is less suitable for end-user navigation, but it could still be useful in building inspection workflows where a system needs to explore all reachable rooms or corridors systematically.

Another application is robotics. A robot moving through a warehouse or factory floor must plan routes while avoiding obstacles. Even though real robotic systems often use more advanced path-planning methods, the core ideas in BFS, DFS, and heuristic search still appear in those systems.

## Conclusion

This project demonstrates the tradeoffs between blind and heuristic search in a maze environment. BFS provides the strongest guarantee of path quality in an unweighted maze, Greedy Best-First Search uses Manhattan distance to direct the search toward the goal, and DFS explores deeply with lower implementation complexity. On the sample maze used in this report, all three algorithms found a path of the same marked length, while DFS had the lowest measured runtime and BFS had the highest memory usage.

The most important lesson from this comparison is that there is no single best search algorithm for every situation. The correct choice depends on the structure of the search space and on whether the priority is shortest-path optimality, speed, or memory efficiency.

## References

Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.

Northeastern University. (2026). *Module 3.11 Assignment: Maze Search Implementation*.
