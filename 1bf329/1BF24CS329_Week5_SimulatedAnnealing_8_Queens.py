import math
import random


def calculate_cost(state):
    """Calculates the number of attacking queen pairs diagonally."""
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def run_chained_evaluation():
    print("==================================================")
    print("   SA CHAINED TRACE TABLE GENERATOR               ")
    print("==================================================")

    num_cases = int(input("👉 How many steps/iterations do you want to trace? "))
    results_table = []

    # 1. Input the Initial Current State ONCE at the very beginning
    print("\n👉 Enter the starting Current State for Step #1 (e.g., 0 1 2 3 4 5 6 7):")
    current = tuple(map(int, input().strip().split()))
    current_cost = calculate_cost(current)

    for idx in range(1, num_cases + 1):
        print(f"\n--- Data Entry for Step #{idx} ---")
        print(f"Active Current State: {current} (Cost: {current_cost})")

        # 2. Input Next State for this specific step
        print("Enter Next State (e.g., 4 1 2 3 4 5 6 7):")
        nxt = tuple(map(int, input().strip().split()))
        nxt_cost = calculate_cost(nxt)

        # 3. Input Temperature for this specific step
        print("Enter Temperature T (e.g., 100.0):")
        T = float(input())

        # Math Processing
        delta_E = current_cost - nxt_cost

        # Determine alignment and state updates
        if delta_E > 0:
            prob_str = "1.0000"
            rand_str = "N/A"
            outcome = "ACCEPTED"
            # Update current state for the NEXT loop iteration
            previous_current = current
            current = nxt
            current_cost = nxt_cost
        else:
            p = math.exp(delta_E / T)
            prob_str = f"{p:.4f}"
            rand_val = random.random()
            rand_str = f"{rand_val:.4f}"

            if rand_val < p:
                outcome = "ACCEPTED"
                previous_current = current
                current = nxt
                current_cost = nxt_cost
            else:
                outcome = "REJECTED"
                previous_current = current
                # current state stays the same for the next iteration if rejected

        # Store trace properties
        results_table.append(
            {
                "id": idx,
                "current": str(previous_current),
                "c_cost": calculate_cost(previous_current),
                "next": str(nxt),
                "n_cost": nxt_cost,
                "temp": f"{T:.1f}",
                "delta": delta_E,
                "prob": prob_str,
                "rand": rand_str,
                "outcome": outcome,
            }
        )

    # =====================================================================
    # OUTPUT TRACE TABLE
    # =====================================================================
    print("\n" + "=" * 115)
    print(f"{'SIMULATED ANNEALING CHAINED RUN TRACE':^115}")
    print("=" * 115)

    header_format = "{:<4} {:<22} {:<6} {:<22} {:<6} {:<6} {:<5} {:<8} {:<8} {:<10}"
    print(
        header_format.format(
            "ID",
            "Current State",
            "Cost",
            "Next State",
            "Cost",
            "Temp",
            "ΔE",
            "Prob(p)",
            "RandVal",
            "Outcome",
        )
    )
    print("-" * 115)

    for row in results_table:
        print(
            header_format.format(
                row["id"],
                row["current"],
                row["c_cost"],
                row["next"],
                row["n_cost"],
                row["temp"],
                row["delta"],
                row["prob"],
                row["rand"],
                row["outcome"],
            )
        )

    print("=" * 115)
    print(f"Final State Remaining after trace: {current} (Cost: {current_cost})")
    print("=" * 115)


run_chained_evaluation()
