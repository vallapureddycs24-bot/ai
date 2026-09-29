from collections import deque
import sys

# Define the goal state
GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)  # 0 represents the blank tile

# Moves: Up, Down, Left, Right
MOVES = {
    'U': -3,
    'D': 3,
    'L': -1,
    'R': 1
}

# Valid moves depending on blank position
INVALID_MOVES = {
    0: ['U', 'L'],
    1: ['U'],
    2: ['U', 'R'],
    3: ['L'],
    5: ['R'],
    6: ['L', 'D'],
    7: ['D'],
    8: ['R', 'D']
}

def is_solvable(state):
    """Check if the puzzle is solvable using inversion count."""
    arr = [x for x in state if x != 0]
    inversions = sum(1 for i in range(len(arr)) for j in range(i+1, len(arr)) if arr[i] > arr[j])
    return inversions % 2 == 0

def get_new_state(state, move):
    """Generate a new state after applying a move."""
    blank_index = state.index(0)
    if move in INVALID_MOVES.get(blank_index, []):
        return None
    new_index = blank_index + MOVES[move]
    if new_index < 0 or new_index >= 9:
        return None
    new_state = list(state)
    new_state[blank_index], new_state[new_index] = new_state[new_index], new_state[blank_index]
    return tuple(new_state)

def dls(state, depth, path, visited):
    """Depth-Limited Search."""
    if state == GOAL_STATE:
        return path
    if depth == 0:
        return None
    visited.add(state)
    for move in MOVES.keys():
        new_state = get_new_state(state, move)
        if new_state and new_state not in visited:
            result = dls(new_state, depth - 1, path + [move], visited)
            if result:
                return result
    return None

def iddfs(start_state, max_depth=50):
    """Iterative Deepening DFS."""
    for depth in range(max_depth + 1):
        visited = set()
        result = dls(start_state, depth, [], visited)
        if result is not None:
            return result
    return None

def main():
    try:
        # Input puzzle state
        print("Enter the puzzle state (0 for blank), row-wise, separated by spaces:")
        raw_input = input().strip().split()
        if len(raw_input) != 9 or not all(x.isdigit() for x in raw_input):
            print("Invalid input. Please enter exactly 9 integers (0-8).")
            return
        start_state = tuple(map(int, raw_input))
        if sorted(start_state) != list(range(9)):
            print("Invalid puzzle configuration. Must contain numbers 0-8 exactly once.")
            return

        # Check solvability
        if not is_solvable(start_state):
            print("This puzzle is unsolvable.")
            return

        # Solve using IDDFS
        solution = iddfs(start_state)
        if solution:
            print(f"Solution found in {len(solution)} moves: {' '.join(solution)}")
        else:
            print("No solution found within depth limit.")

    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
