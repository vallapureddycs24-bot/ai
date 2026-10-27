import copy


def count_conflicts(state):
    """Counts the number of pairs of queens attacking each other diagonally."""
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def get_all_swap_neighbors(state):
    """Generates all neighbors by swapping row positions of two queens.

    Returns a list of tuples: (neighbor_state, (i, j)) sorted lexicographically
    by the swap indices (i, j) to ensure proper tie-breaking.
    """
    neighbors = []
    n = len(state)
    # Generating in strict order: (0,1), (0,2), (0,3), (1,2), (1,3), (2,3)
    for i in range(n):
        for j in range(i + 1, n):
            neighbor_state = list(state)
            # Swap row positions of columns i and j
            neighbor_state[i], neighbor_state[j] = (
                neighbor_state[j],
                neighbor_state[i],
            )
            neighbors.append((tuple(neighbor_state), (i, j)))
    return neighbors


def hill_climbing_4queens(initial_state):
    current_state = tuple(initial_state)
    current_cost = count_conflicts(current_state)

    print("==================================================")
    print("STARTING HILL-CLIMBING SEARCH")
    print("==================================================")
    print(f"Initial State: {current_state} | Cost: {current_cost}\n")

    step = 0
    while True:
        if current_cost == 0:
            print("Goal state reached! No remaining conflicts.")
            break

        step += 1
        print(f"--- Step {step}: Evaluating Neighbors ---")
        neighbors = get_all_swap_neighbors(current_state)

        best_neighbor = None
        best_cost = current_cost
        chosen_swap = None

        # Print table header for trace
        print(f"{'Swap (i, j)':<15}{'Neighbor State':<20}{'Cost':<5}")
        print("-" * 40)

        for neighbor_state, swap_pair in neighbors:
            cost = count_conflicts(neighbor_state)
            print(f"Swap {swap_pair!s:<10}{neighbor_state!s:<20}{cost:<5}")

            # Strict '<' because neighbors are already sorted lexicographically by swap_pair.
            # If a later neighbor has the same cost, it won't overwrite the earlier one,
            # satisfying the tie-breaking rule: choose the smallest subscript/column number.
            if cost < best_cost:
                best_cost = cost
                best_neighbor = neighbor_state
                chosen_swap = swap_pair

        print("-" * 40)

        # If no neighbor is strictly better than the current state, we are stuck
        # at a local optimum/flat local maximum, so the algorithm terminates.
        if best_cost >= current_cost:
            print(
                f"\nNo better neighbor found. Stuck at local maximum/optimum."
            )
            print(f"Terminating at state: {current_state} with cost: {current_cost}")
            break

        # Move to the best neighbor
        print(
            f"Decision: Accept Swap {chosen_swap} -> New State: {best_neighbor} with Cost: {best_cost}\n"
        )
        current_state = best_neighbor
        current_cost = best_cost

    print("\n==================================================")
    print(f"Final State Configuration: {current_state}")
    print(f"Final Cost: {current_cost}")
    print("==================================================")


# Define initial state from observation book: x0=3, x1=1, x2=2, x3=0
init_state = [3, 1, 2, 0]
hill_climbing_4queens(init_state)
