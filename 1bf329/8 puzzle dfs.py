from collections import deque

# Define the goal state
GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)  # 0 represents the empty tile

# Possible moves: up, down, left, right
MOVES = {
    'UP': -3,
    'DOWN': 3,
    'LEFT': -1,
    'RIGHT': 1
}

def is_valid_move(pos, move):
    """Check if a move is valid based on the empty tile position."""
    if move == 'UP' and pos < 3:
        return False
    if move == 'DOWN' and pos > 5:
        return False
    if move == 'LEFT' and pos % 3 == 0:
        return False
    if move == 'RIGHT' and pos % 3 == 2:
        return False
    return True

def get_new_state(state, move):
    """Return a new state after applying the move."""
    state = list(state)
    empty_pos = state.index(0)
    new_pos = empty_pos + MOVES[move]
    state[empty_pos], state[new_pos] = state[new_pos], state[empty_pos]
    return tuple(state)

def dfs(start_state):
    """Depth-First Search to solve the 8-puzzle."""
    stack = [(start_state, [])]  # (state, path)
    visited = set()

    while stack:
        state, path = stack.pop()

        if state == GOAL_STATE:
            return path + [state]

        if state in visited:
            continue
        visited.add(state)

        empty_pos = state.index(0)
        for move in MOVES:
            if is_valid_move(empty_pos, move):
                new_state = get_new_state(state, move)
                if new_state not in visited:
                    stack.append((new_state, path + [state]))
    return None

def print_board(state):
    """Pretty print the puzzle board."""
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

if __name__ == "__main__":
    # Example start state (solvable)
    start_state = (1, 2, 3,
                   4, 0, 6,
                   7, 5, 8)

    print("Initial State:")
    print_board(start_state)

    solution = dfs(start_state)

    if solution:
        print(f"Solution found in {len(solution)-1} moves:")
        for step in solution:
            print_board(step)
    else:
        print("No solution found.")
