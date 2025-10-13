from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json, os
from functools import wraps
from spotify import search_for_song, get_token

load_dotenv()

spotify_token = get_token()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for session handling

USERS_FILE = "users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        users = load_users()

        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("editlesson"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        users = load_users()

        if username in users:
            return render_template("signup.html", error="Username already exists")

        users[username] = password
        save_users(users)
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/editlesson", methods=["GET", "POST"])
@login_required
def editlesson():
    if request.method == "POST":
        searchprompt = request.form.get("searchsong")
    return render_template("editlesson.html", username=session["username"])




@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/search_songs")
@login_required
def search_songs():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    songs = search_for_song(spotify_token, query)
    results = [
        {
            "name": song["name"],
            "url": f"https://open.spotify.com/track/{song['id']}"
        }
        for song in songs
    ]
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
