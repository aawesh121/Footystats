from flask import Flask, abort, render_template, request

import analysis
import database

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    results = database.search_players(query) if query else []
    return render_template("search.html", query=query, results=results)


@app.route("/player/<int:player_id>")
def player(player_id):
    p = database.get_player(player_id)
    if p is None:
        abort(404)
    rows = database.get_performances(player_id)
    summary = analysis.summarize(rows)
    chart = {
        "labels": [s["season"] for s in summary["seasons"]],
        "goals": [s["goals"] for s in summary["seasons"]],
        "assists": [s["assists"] for s in summary["seasons"]],
    }
    return render_template("player.html", p=p, rows=rows, summary=summary, chart=chart)


@app.errorhandler(404)
def not_found(_):
    return render_template("base.html", not_found=True), 404


if __name__ == "__main__":
    app.run(debug=True)
