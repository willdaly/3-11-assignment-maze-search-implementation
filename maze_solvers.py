"""3.11 Assignment: Maze Search Implementation maze solver interface."""

from pathlib import Path
from collections import deque

#load maze from file
maze_text = Path(__file__).with_name("maze.txt").read_text(encoding="utf-8")

#convert maze text to 2D list
lines = [ln.rstrip("\n") for ln in maze_text.splitlines() if ln.strip()]
width, height = map(int, lines[0].split())   # "10 6"
maze_lines = lines[1:]                       # actual maze rows

#create 2D list representation of the maze
maze = [list(row) for row in maze_lines]

PATH_CHAR = "*"

ACTIONS = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

def find_state(maze, target):
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


#blind search algorithm:
#breadth-first search (BFS) implementation
def maze_solver_one(maze):
    # set the initial state to the position of "S" in the maze
    initial_state = find_state(maze, "S")
    # set the goal state to the position of "E" in the maze
    goal_state = find_state(maze, "E")
    # frontier is a queue that will hold the states to explore, starting with the initial state
    frontier = deque([initial_state])   # queue for BFS

    visited = {initial_state}  # set to keep track of visited states

    parent = {initial_state: None}  # dictionary to keep track of the parent of each state for path reconstruction

    # BFS loop runs until there are no more states to explore in the frontier
    while frontier: 
        state = frontier.popleft() # get the next state to explore from the frontier (FIFO order for BFS)

        if state == goal_state: # if we have reached the goal state, we can stop searching
            break

        for action in ACTIONS: # iterate over all possible actions (U, D, L, R)
            next_state = transition(state, action, maze) # compute the next state resulting from taking the action from the current state
            if next_state is not None and next_state not in visited: # if the next state is valid (not a wall or out of bounds) and has not been visited yet
                visited.add(next_state) # mark the next state as visited
                parent[next_state] = state # record the current state as the parent of the next state for path reconstruction
                frontier.append(next_state) # add the next state to the frontier to be explored in future iterations

    # reconstruct path using parent dictionary
    path = [] # list to hold the path from start to goal
    current = goal_state # start from the goal state and follow the parent links back to the initial state
    while current is not None: # while we haven't reached the initial state (which has parent None)
        path.append(current) # add the current state to the path
        current = parent[current] # move to the parent of the current state
    path.reverse() # reverse the path to get it from start to goal order

    # mark the path in the maze with PATH_CHAR
    for row_index, col_index in path:
        if maze[row_index][col_index] in ("S", "E"):
            continue  # don't overwrite start or goal
        maze[row_index][col_index] = PATH_CHAR

    return maze

#heuristic search algorithm:
def maze_solver_two(maze):
    """Solve the maze and return the solved maze output."""
    return maze

#dealer's choice algorithm:
def maze_solver_three(maze):
    """Solve the maze and return the solved maze output."""
    return maze

def main():
    solved_maze = maze_solver_one([row[:] for row in maze])
    print(format_maze_output(solved_maze, width=width, height=height))


if __name__ == "__main__":
    main()