"""Evaluate maze solver performance and search-complexity proxies.

This script compares:
- maze_solver_one (BFS)
- maze_solver_two (Greedy Best-First)
- maze_solver_three (DFS)

Metrics reported:
- Runtime (ms)
- Peak memory (KiB) via tracemalloc
- Transition calls (proxy for explored edges)
- Estimated expanded states (transition_calls / number_of_actions)
- Path length (# of '*' cells)

It also prints graph-level V and E values for the current maze, where:
- V = number of non-wall cells
- E = number of directed valid moves between adjacent non-wall cells
"""

from __future__ import annotations

from time import perf_counter
import tracemalloc
from pathlib import Path
from typing import Callable, List, Tuple

import maze_solvers as ms


MazeGrid = List[List[str]]
State = Tuple[int, int]


def clone_maze(maze: MazeGrid) -> MazeGrid:
    return [row[:] for row in maze]


def compute_graph_size(maze: MazeGrid) -> Tuple[int, int]:
    """Return (V, E) for the maze graph.

    V: count of non-wall cells.
    E: count of directed valid moves between non-wall neighbor cells.
    """
    height = len(maze)
    width = len(maze[0]) if height else 0

    def is_open(row_index: int, col_index: int) -> bool:
        return maze[row_index][col_index] != "X"

    node_count = 0
    edge_count = 0

    for row_index in range(height):
        for col_index in range(width):
            if not is_open(row_index, col_index):
                continue
            node_count += 1
            for row_delta, col_delta in ms.ACTIONS.values():
                next_row = row_index + row_delta
                next_col = col_index + col_delta
                if 0 <= next_row < height and 0 <= next_col < width and is_open(next_row, next_col):
                    edge_count += 1

    return node_count, edge_count


def evaluate_solver(solver_name: str, solver: Callable[[MazeGrid], MazeGrid], base_maze: MazeGrid) -> dict[str, float | str]:
    """Run one solver and collect evaluation metrics."""
    transition_calls = 0
    original_transition = ms.transition

    def counting_transition(state: State, action: str, maze: MazeGrid):
        nonlocal transition_calls
        transition_calls += 1
        return original_transition(state, action, maze)

    try:
        ms.transition = counting_transition

        maze_input = clone_maze(base_maze)

        tracemalloc.start()
        start_time = perf_counter()
        solved_maze = solver(maze_input)
        elapsed_ms = (perf_counter() - start_time) * 1000
        _current_bytes, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()
    finally:
        ms.transition = original_transition

    action_count = len(ms.ACTIONS)
    estimated_expanded_states = transition_calls / action_count if action_count else 0
    path_length = sum(cell == ms.PATH_CHAR for row in solved_maze for cell in row)

    return {
        "solver": solver_name,
        "runtime_ms": elapsed_ms,
        "peak_memory_kib": peak_bytes / 1024,
        "transition_calls": float(transition_calls),
        "expanded_states_est": estimated_expanded_states,
        "path_length": float(path_length),
    }


def main() -> None:
    _width, _height, loaded_maze = ms.load_maze_from_file(Path(__file__).with_name("maze.txt"))
    base_maze = clone_maze(loaded_maze)
    node_count, edge_count = compute_graph_size(base_maze)

    print("=== Maze Graph Size ===")
    print(f"V (nodes/non-wall cells): {node_count}")
    print(f"E (directed transitions): {edge_count}")
    print("Theoretical blind search bound reference: O(V + E)")
    print()

    solvers = [
        ("maze_solver_one (BFS)", ms.maze_solver_one),
        ("maze_solver_two (Greedy Best-First)", ms.maze_solver_two),
        ("maze_solver_three (DFS)", ms.maze_solver_three),
    ]

    results = [evaluate_solver(name, solver, base_maze) for name, solver in solvers]

    print("=== Empirical Evaluation ===")
    print(
        "Solver".ljust(34),
        "Runtime(ms)".rjust(12),
        "Peak KiB".rjust(10),
        "Transitions".rjust(12),
        "Expanded~".rjust(10),
        "Path(*)".rjust(8),
    )
    print("-" * 90)

    for result in results:
        print(
            str(result["solver"]).ljust(34),
            f"{result['runtime_ms']:.3f}".rjust(12),
            f"{result['peak_memory_kib']:.2f}".rjust(10),
            f"{int(result['transition_calls'])}".rjust(12),
            f"{result['expanded_states_est']:.1f}".rjust(10),
            f"{int(result['path_length'])}".rjust(8),
        )

    print()
    print("Note: Transition calls and expanded-state estimate are empirical proxies, not formal proofs of Big O.")


if __name__ == "__main__":
    main()
