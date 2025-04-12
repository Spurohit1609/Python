import tensorflow as tf
import numpy as np
import random

def print_board(board):
    for i, row in enumerate(board):
        print(" | ".join(row))
        if i < 2:
            print("-" * 9)

def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def player_move(board, player):
    while True:
        try:
            row = int(input(f"Player {player}, enter row (1-3): ")) - 1
            col = int(input(f"Player {player}, enter column (1-3): ")) - 1
            if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == " ":
                board[row][col] = player
                break
            else:
                print("Invalid move! Try again.")
        except ValueError:
            print("Please enter numbers between 1 and 3.")

def board_to_input(board, player):
    mapping = {" ": 0, player: 1, ("O" if player == "X" else "X"): -1}
    return np.array([[mapping[cell] for cell in row] for row in board], dtype=np.float32).flatten()

def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(9,)),
        tf.keras.layers.Dense(27, activation='relu'),
        tf.keras.layers.Dense(9)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

model = build_model()

def computer_move(board, player):
    print(f"Computer ({player}) is making a move...")
    input_board = board_to_input(board, player).reshape(1, -1)
    predictions = model.predict(input_board, verbose=0)[0]

    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
    empty_indices = [r * 3 + c for r, c in empty_cells]

    best_index = max(empty_indices, key=lambda i: predictions[i])
    row, col = divmod(best_index, 3)
    board[row][col] = player

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    print("Welcome to Tic-Tac-Toe!")
    mode = input("Choose mode:\n1 - Two Players\n2 - Play vs Computer\nEnter 1 or 2: ")

    board = initialize_board()
    players = ["X", "O"]
    current_player = 0

    while True:
        print_board(board)
        if mode == "2" and players[current_player] == "O":
            computer_move(board, players[current_player])
        else:
            player_move(board, players[current_player])

        if check_winner(board, players[current_player]):
            print_board(board)
            if mode == "2" and players[current_player] == "O":
                print("Computer wins!")
            else:
                print(f"Player {players[current_player]} wins!")
            break

        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % 2

def main():
    while True:
        play_game()
        replay = input("Do you want to play again? (yes/no): ").lower()
        if replay != "yes":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
