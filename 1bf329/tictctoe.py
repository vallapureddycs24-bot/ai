import random

# Display the board
def print_board(board):
    print("\n")
    for i in range(3):
        print(" | ".join(board[i]))
        if i < 2:
            print("-" * 5)
    print("\n")

# Check if a player has won
def check_winner(board, player):
    # Rows, columns, diagonals
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):  # Row
            return True
        if all(board[j][i] == player for j in range(3)):  # Column
            return True
    if all(board[i][i] == player for i in range(3)):      # Main diagonal
        return True
    if all(board[i][2 - i] == player for i in range(3)):  # Anti-diagonal
        return True
    return False

# Check if the board is full
def is_full(board):
    return all(board[i][j] != " " for i in range(3) for j in range(3))

# Player move
def player_move(board, player):
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-9): "))
            if move < 1 or move > 9:
                print("Invalid move. Choose between 1 and 9.")
                continue
            row, col = divmod(move - 1, 3)
            if board[row][col] == " ":
                board[row][col] = player
                break
            else:
                print("Cell already taken. Try again.")
        except ValueError:
            print("Invalid input. Enter a number between 1 and 9.")

# Computer move (basic AI: random choice)
def computer_move(board, player):
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    if available_moves:
        move = random.choice(available_moves)
        board[move[0]][move[1]] = player
        print(f"Computer chooses position {(move[0] * 3 + move[1] + 1)}")

# Main game loop
def tic_tac_toe(mode="2-player"):
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        if mode == "2-player" or (mode == "computer" and current_player == "X"):
            player_move(board, current_player)
        else:
            computer_move(board, current_player)

        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

# Run the game
if __name__ == "__main__":
    print("Choose mode:")
    print("1. Two Player")
    print("2. Play vs Computer")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        tic_tac_toe("2-player")
    elif choice == "2":
        tic_tac_toe("computer")
    else:
        print("Invalid choice. Exiting.")
