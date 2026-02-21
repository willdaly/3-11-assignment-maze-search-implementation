"""3.11 Assignment: Maze Search Implementation maze solver interface."""

from pathlib import Path
from collections import deque
import heapq
from typing import Optional

#load maze from file
maze_text = Path(__file__).with_name("maze.txt").read_text(encoding="utf-8")

#convert maze text to 2D list
lines = [ln.rstrip("\n") for ln in maze_text.splitlines() if ln.strip()]
width, height = map(int, lines[0].split())   # "10 6"
maze_lines = lines[1:]                       # actual maze rows

#create 2D list representation of the maze
maze = [list(row) for row in maze_lines]

PATH_CHAR = "*"
State = tuple[int, int]

ACTIONS = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

def find_state(maze, target) -> Optional[State]:
    for r, row in enumerate(maze):
        for c, ch in enumerate(row):
            if ch == target:
                return (r, c)
    return None

def transition(state, action, maze):
    # Look up the row/column movement for this action (e.g., "U" -> -1,0) and unpack it into row_delta, col_delta.
    row_delta, col_delta = ACTIONS[action]
    nr, nc = state[0] + row_delta, state[1] + col_delta

    # invalid move -> None
    if nr < 0 or nr >= len(maze) or nc < 0 or nc >= len(maze[0]):
        return None
    if maze[nr][nc] == "X":  # wall symbol
        return None

    return (nr, nc)


def format_maze_output(maze, width=None, height=None):
    """Format a maze grid for terminal display like the assignment examples."""
    output_lines = []
    if width is not None and height is not None:
        output_lines.append(f"{width} {height}")
        output_lines.append("")

    for row in maze:
        output_lines.append("".join(row))
        output_lines.append("")

    return "\n".join(output_lines).rstrip()


def mark_solution_path(maze, parent, goal_state):
    """Reconstruct and mark the path from start to goal using parent links."""
    if goal_state not in parent:
        return maze

    path = []
    current_state = goal_state
    while current_state is not None:
        path.append(current_state)
        current_state = parent[current_state]
    path.reverse()

    for row_index, col_index in path:
        if maze[row_index][col_index] in ("S", "E"):
            continue
        maze[row_index][col_index] = PATH_CHAR

    return maze


def initialize_search_context(maze):
    """Initialize common search variables for BFS/DFS."""
    # initial state is the root node of the search tree
    initial_state = find_state(maze, "S")
    goal_state = find_state(maze, "E")

    if initial_state is None or goal_state is None:
        raise ValueError("Maze must include both 'S' and 'E'.")

    visited: set[State] = {initial_state}
    parent: dict[State, Optional[State]] = {initial_state: None}
    return initial_state, goal_state, visited, parent


def manhattan_distance(current_state, goal_state):
    """Return Manhattan distance between two maze coordinates."""
    return abs(current_state[0] - goal_state[0]) + abs(current_state[1] - goal_state[1])


#blind search algorithm:
#breadth-first search (BFS) implementation
def maze_solver_one(maze):
    initial_state, goal_state, visited, parent = initialize_search_context(maze)
    frontier = deque([initial_state])

    # BFS loop runs until there are no more states to explore in the frontier
    while frontier: 
        # Deque the front node
        # Nodes are dequeued when it’s their turn to be explored.
        state = frontier.popleft() # get the next state to explore from the frontier (FIFO order for BFS)

        # Check if it’s the goal. If yes, stop.
        if state == goal_state: # if we have reached the goal state, we can stop searching
            break

        for action in ACTIONS: # iterate over all possible actions (U, D, L, R)
            # compute the next state resulting from taking the action from the current state
            next_state = transition(state, action, maze) # alsso called child node
            if next_state is not None and next_state not in visited: # if the next state is valid (not a wall or out of bounds) and has not been visited yet
                visited.add(next_state) # mark the next state as visited
                parent[next_state] = state # record the current state as the parent of the next state for path reconstruction
                # If not, enqueue all its children.
                # In BFS, nodes are enqueued when discovered, so we add the next state to the end of the frontier
                frontier.append(next_state) # add the next state to the frontier to be explored in future iterations

    return mark_solution_path(maze, parent, goal_state)

#heuristic search algorithm: Greedy Best-First Search implementation with Manhattan distance heuristic
def maze_solver_two(maze):
    initial_state = find_state(maze, "S")
    goal_state = find_state(maze, "E")
    if initial_state is None or goal_state is None:
        raise ValueError("Maze must include both 'S' and 'E'.")
    frontier = []
    heapq.heappush(frontier, (manhattan_distance(initial_state, goal_state), initial_state))  # (priority, state)
    visited = {initial_state}
    parent = {initial_state: None}  
    while frontier:
        priority, state = heapq.heappop(frontier)
        if state == goal_state:
            break
        for action in ACTIONS:
            next_state = transition(state, action, maze)
            if next_state is not None and next_state not in visited:
                visited.add(next_state)
                parent[next_state] = state
                heapq.heappush(frontier, (manhattan_distance(next_state, goal_state), next_state))
    return mark_solution_path(maze, parent, goal_state)

#blind search algorithm:
#Depth-first search (DFS) implementation
def maze_solver_three(maze):
    initial_state, goal_state, visited, parent = initialize_search_context(maze)
    frontier = [initial_state]
    while frontier:
        # pop the top node from the stack and explore it
        state = frontier.pop()  # get the next state to explore from the frontier (LIFO order for DFS)
        # If it’s the goal, stop.
        if state == goal_state:
            break

        for action in ACTIONS:
            next_state = transition(state, action, maze)
            # Otherwise, push its children onto the stack.
            if next_state is not None and next_state not in visited:
                visited.add(next_state)
                parent[next_state] = state
                frontier.append(next_state)
    return mark_solution_path(maze, parent, goal_state)

def main():
    solved_maze = maze_solver_one([row[:] for row in maze])
    print(format_maze_output(solved_maze, width=width, height=height))

    solved_maze = maze_solver_two([row[:] for row in maze])
    print(format_maze_output(solved_maze, width=width, height=height))

    solved_maze = maze_solver_three([row[:] for row in maze])
    print(format_maze_output(solved_maze, width=width, height=height))


if __name__ == "__main__":
    main()