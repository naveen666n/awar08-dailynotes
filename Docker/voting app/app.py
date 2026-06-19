from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

OPTION_A = "AWS"
OPTION_B = "Azure"

# Votes are stored in memory. Simple and dependency-free — perfect for a
# first Docker demo. NOTE: counts reset when the container restarts, because
# nothing is persisted. That "lost data" moment is the lesson that motivates
# adding Redis (and later, volumes) in the next stage.
votes = {OPTION_A: 0, OPTION_B: 0}


@app.route("/")
def index():
    return render_template("index.html", option_a=OPTION_A, option_b=OPTION_B)


@app.route("/vote", methods=["POST"])
def vote():
    choice = request.form.get("vote")
    if choice not in votes:
        return jsonify({"error": "invalid choice"}), 400
    votes[choice] += 1
    return jsonify({"status": "ok", "voted": choice})


@app.route("/results")
def results():
    a, b = votes[OPTION_A], votes[OPTION_B]
    total = a + b
    return jsonify({
        "option_a": OPTION_A, "option_b": OPTION_B,
        "votes_a": a, "votes_b": b, "total": total,
        "pct_a": round(a / total * 100, 1) if total else 0,
        "pct_b": round(b / total * 100, 1) if total else 0,
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)