from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"game_id": game_id, "board": game.board})

@app.post("/api/score-word")
def score_word():
    """ Check if word is legal  (in word list and findable on board)
        Returns JSON of result e.g.
            {result: 'not-word'}, {result: 'not-on-bard}, {result: 'ok'}
    """
    word = request.json['word']
    game_id = request.json['game_id']

    if not games[game_id].is_word_in_word_list(word):
        return jsonify({"result": "not-word"})

    if not games[game_id].check_word_on_board(word):
        return jsonify({"result": "not-on-board"})

    else:
        return jsonify({"result": "ok"})
