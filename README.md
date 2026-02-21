# Maze Search Implementation

This project solves text-based mazes using three search algorithms in `maze_solvers.py`:

- `maze_solver_one(maze)`: Breadth-First Search (BFS, blind search)
- `maze_solver_two(maze)`: Greedy Best-First Search (heuristic, Manhattan distance)
- `maze_solver_three(maze)`: Depth-First Search (DFS, blind search)

Each solver takes one maze (2D list of characters) and returns a solved maze where the path is marked with `*`.

## Maze format

The input maze file format is:

1. First line: `width height` (for example, `10 6`)
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

Create/activate your Python environment, then install dependencies:

```bash
pip install -r requirements.txt
```

## Run the program

Run all three solvers on `maze.txt`:

```bash
python maze_solvers.py
```

The script prints each solved maze in assignment-style text output (including the `width height` line and path marked by `*`).

## Use as functions (API)

You can also import and call the solver functions directly:

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

Use `[row[:] for row in maze]` to pass a copy, since each solver marks the path in-place.

## Tests

Run tests with:

```bash
pytest
```

Note: current test scaffold may be minimal and can be expanded with algorithm-specific test cases.
