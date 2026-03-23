# Maze Search Implementation

This project solves text-based mazes using three search algorithms in `maze_solvers.py`:

- `maze_solver_one(maze)`: Breadth-First Search (BFS, blind search)
- `maze_solver_two(maze)`: Greedy Best-First Search (heuristic, Manhattan distance)
- `maze_solver_three(maze)`: Depth-First Search (DFS, blind search)

Each solver takes one maze (a 2D list of characters) and returns a solved maze with the path marked by `*`.

## Maze format

The maze text format matches the assignment brief:

1. First line: `width height`
2. Remaining lines: maze rows using:
   - `S` = start
   - `E` = exit
   - `X` = wall
   - space (` `) = open cell

Example:

```text
10 6
XXXXXXXXXX
X        S
X XXXXXX X
X X    XXX
X   XX   E
XXXXXXXXXX
```

## Setup

Install the project dependency:

```bash
pip install -r requirements.txt
```

## Run the solvers

To run all three solvers on the sample maze file included in the repository:

```bash
python maze_solvers.py
```

The script prints three solved mazes, one per algorithm, in the same text format used in the assignment.

## Use the required solver functions

You can import and call the assignment interface directly:

```python
from maze_solvers import maze_solver_one, maze_solver_two, maze_solver_three

maze = [
    list("XXXXXXXXXX"),
    list("X        S"),
    list("X XXXXXX X"),
    list("X X    XXX"),
    list("X   XX   E"),
    list("XXXXXXXXXX"),
]

solved_bfs = maze_solver_one([row[:] for row in maze])
solved_greedy = maze_solver_two([row[:] for row in maze])
solved_dfs = maze_solver_three([row[:] for row in maze])
```

Pass a copy such as `[row[:] for row in maze]` because each solver marks the solution path in place.

## Helper utilities

The module also includes:

- `parse_maze_text(maze_text)` to parse assignment-format maze text
- `load_maze_from_file(file_path)` to load a maze from a `.txt` file

These helpers are optional and are not required by the assignment grader.

## Evaluation scripts

Two additional scripts are included for local analysis:

- `python evaluate_solvers.py` for a single-run comparison
- `python evaluate_report_metrics.py` for repeated timing and memory metrics used in the report

## Tests

No formal pytest test suite is included in this repository. The `pytest` dependency is present only if you want to add tests locally.
