"""Evaluate maze solvers by report categories.

Categories:
1) Time complexity (empirical timing + theoretical class note)
2) Space complexity (peak memory + frontier/visited proxy)
3) Solution quality (path length + optimality vs BFS)
4) Search space traversal (expanded states and transition calls)
"""

from __future__ import annotations

from time import perf_counter
import tracemalloc
from typing import Callable, List, Tuple

import maze_solvers as ms


MazeGrid = List[List[str]]
State = Tuple[int, int]


def clone_maze(maze: MazeGrid) -> MazeGrid:
    return [row[:] for row in maze]


def count_non_wall_nodes(maze: MazeGrid) -> int:
    return sum(cell != "X" for row in maze for cell in row)


def count_path_stars(maze: MazeGrid) -> int:
    return sum(cell == ms.PATH_CHAR for row in maze for cell in row)


def evaluate_solver(
    solver_name: str,
    solver: Callable[[MazeGrid], MazeGrid],
    base_maze: MazeGrid,
    runs: int = 20,
) -> dict[str, float | str]:
    """Run a solver repeatedly and collect empirical metrics."""
    total_time_ms = 0.0
    peak_memory_kib = 0.0
    transition_calls = 0

    original_transition = ms.transition

    def counting_transition(state: State, action: str, maze: MazeGrid):
        nonlocal transition_calls
        transition_calls += 1
        return original_transition(state, action, maze)

    try:
        ms.transition = counting_transition

        solved_maze = None
        for _ in range(runs):
            maze_input = clone_maze(base_maze)
            tracemalloc.start()
            start = perf_counter()
            solved_maze = solver(maze_input)
            elapsed_ms = (perf_counter() - start) * 1000
            _current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            total_time_ms += elapsed_ms
            peak_memory_kib = max(peak_memory_kib, peak / 1024)
    finally:
        ms.transition = original_transition

    if solved_maze is None:
        raise RuntimeError(f"{solver_name} did not produce a maze result.")

    path_length = count_path_stars(solved_maze)
    action_count = len(ms.ACTIONS)
    avg_transition_calls = transition_calls / runs if runs else float(transition_calls)
    expanded_states_est = avg_transition_calls / action_count if action_count else 0.0

    return {
        "solver": solver_name,
        "avg_runtime_ms": total_time_ms / runs,
        "peak_memory_kib": peak_memory_kib,
        "transition_calls": avg_transition_calls,
        "expanded_states_est": expanded_states_est,
        "path_length": float(path_length),
    }


def print_table_row(values: List[str], widths: List[int]) -> None:
    columns = [value.ljust(width) for value, width in zip(values, widths)]
    print(" | ".join(columns))


def main() -> None:
    base_maze = clone_maze(ms.maze)
    node_count = count_non_wall_nodes(base_maze)

    solvers = [
        ("BFS", ms.maze_solver_one, "O(V + E)"),
        ("Greedy", ms.maze_solver_two, "O(V + E) typical graph traversal"),
        ("DFS", ms.maze_solver_three, "O(V + E)"),
    ]

    results = []
    for label, solver, complexity in solvers:
        metrics = evaluate_solver(label, solver, base_maze, runs=20)
        metrics["theory_time"] = complexity
        results.append(metrics)

    bfs_path_length = next(result["path_length"] for result in results if result["solver"] == "BFS")

    print("=== Time Complexity ===")
    print("Empirical metric: average runtime across 20 runs")
    widths = [10, 16, 30]
    print_table_row(["Solver", "Avg Time (ms)", "Theoretical"], widths)
    print("-" * (sum(widths) + 6))
    for result in results:
        print_table_row(
            [
                result["solver"],
                f"{result['avg_runtime_ms']:.4f}",
                str(result["theory_time"]),
            ],
            widths,
        )

    print("\n=== Space Complexity ===")
    print("Empirical metric: peak memory via tracemalloc (KiB)")
    widths = [10, 18]
    print_table_row(["Solver", "Peak Memory (KiB)"], widths)
    print("-" * (sum(widths) + 3))
    for result in results:
        print_table_row([result["solver"], f"{result['peak_memory_kib']:.2f}"], widths)

    print("\n=== Solution Quality ===")
    print("Metric: path length using '*' cells (shorter is better on same maze)")
    widths = [10, 14, 24]
    print_table_row(["Solver", "Path Length", "Quality vs BFS"], widths)
    print("-" * (sum(widths) + 6))
    for result in results:
        relation = "optimal (matches BFS)" if result["path_length"] == bfs_path_length else "non-optimal/alternative"
        print_table_row([result["solver"], str(int(result["path_length"])), relation], widths)

    print("\n=== Search Space Traversal ===")
    print("Metric: transition calls and estimated expanded states")
    widths = [10, 18, 18, 18]
    print_table_row(["Solver", "Transition Calls", "Expanded States~", "% of Nodes (V)"], widths)
    print("-" * (sum(widths) + 9))
    for result in results:
        node_percent = (result["expanded_states_est"] / node_count * 100) if node_count else 0.0
        print_table_row(
            [
                result["solver"],
                str(int(result["transition_calls"])),
                f"{result['expanded_states_est']:.1f}",
                f"{node_percent:.1f}%",
            ],
            widths,
        )

    print("\nNotes:")
    print("- Expanded states are estimated as transition_calls / number_of_actions.")
    print("- This script provides empirical evidence for your report, not a formal proof of Big O.")


if __name__ == "__main__":
    main()
