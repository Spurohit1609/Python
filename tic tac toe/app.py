from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Game state (stored in memory for now)
board = [""] * 9
current_player = "X"
game_over = False

def check_winner():
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in win_combinations:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "Draw"
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global board, current_player, game_over

    data = request.get_json()
    index = int(data["index"])

    # Reset condition
    if index == -1:
        board = [""] * 9
        current_player = "X"
        game_over = False
        return jsonify({"board": board})

    if game_over or board[index]:
        return jsonify({"error": "Invalid move"})

    board[index] = current_player
    winner = check_winner()

    if winner:
        game_over = True
        return jsonify({"board": board, "winner": winner})

    # Switch players
    current_player = "O" if current_player == "X" else "X"
    return jsonify({"board": board, "winner": None})

if __name__ == "__main__":
    app.run(debug=True)
