from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Serve the HTML page
@app.route("/")
def index():
    return render_template("index.html")

# Handle move from frontend
@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    board = data["board"]

    # Simple logic: place "O" in first empty cell
    for r in range(3):
        for c in range(3):
            if board[r][c] == " ":
                board[r][c] = "O"
                return jsonify({"board": board})
    return jsonify({"board": board})  # return unchanged if full

if __name__ == "__main__":
    app.run(debug=True)

