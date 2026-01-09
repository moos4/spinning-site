from dotenv import load_dotenv # pip install python-dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json, os, re
from functools import wraps
from spotify import search_for_song, get_token
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message #use pip install: pip install Flask-Mail

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
app.secret_key = os.environ.get("SECRET_KEY")

serializer = URLSafeTimedSerializer(app.secret_key)

app.config["MAIL_SERVER"] = "smtp.gmail.com"      # or your SMTP server
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")        
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME")

mail = Mail(app)


USERS_FILE = "users.json"

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

TOTAL_USERS = len(load_users())


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def send_verification_email(user_email, token):
    verification_url = url_for("verify_email", token=token, _external=True)
    msg = Message(
        subject="Verify Your Email",
        recipients=[user_email],
        body=f"Welcome!\n\nPlease click the link below to verify your email:\n{verification_url}\n\nThis link expires in 1 hour."
    )
    mail.send(msg)


'''
Drad here is a tutorial on how to add pages

@app.route("/thelink/withmaybesublinks", methods=["GET"])
def anythingyouwantaslongasitisunderthat^():
    return render_template("directiontoyourfile.html")

'''

@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_input = request.form.get("usermail", "").strip()
        password = request.form.get("password", "")

        users = load_users()
        user = None
        
        for u in users.values():
            if u["email"].lower() == user_input.lower() or u["username"] == user_input:
                user = u
                break

        if not user:
            return render_template("login.html", error="User not found")

        if not check_password_hash(user["password"], password):
            return render_template("login.html", error="Invalid password")

        if not user.get("verified", False):
           return render_template("login.html", error="Please verify your email before logging in")

        session["username"] = user["username"]
        return redirect(url_for("editlesson"))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        users = load_users()

        if not username or not email or not password:
            return render_template("signup.html", error="All fields are required")

        for user in users.values():
            if user["username"] == username:
                return render_template("signup.html", error="Username already exists")
            if user["email"] == email:
                return render_template("signup.html", error="Email already in use")

        user_id = str(max(map(int, users.keys()), default=-1) + 1)

        users[user_id] = {
            "username": username,
            "email": email,
            "password": generate_password_hash(password),
            "verified": False
        }

        save_users(users)
        # Generate token
        token = serializer.dumps(email, salt="email-verify")

        # Send email
        send_verification_email(email, token)

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/verify/<token>")
def verify_email(token):
    try:
        email = serializer.loads(
            token,
            salt="email-verify",
            max_age=3600  # 1 hour
        )
    except Exception:
        return "Invalid or expired token"

    users = load_users()

    for user in users.values():
        if user["email"] == email:
            user["verified"] = True
            save_users(users)
            return "Email verified! You can now log in."

    return "User not found"


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
            "songId": f"{song['id']}"
        }
        for song in songs
    ]
    return jsonify(results)


@app.route("/get_song_data")
@login_required
def get_song_data():
    song_id = request.args.get("q", "").strip()
    if not song_id:
        return jsonify({"error": "Missing song ID"}), 400

    headers = {"Authorization": f"Bearer {spotify_token}"}

    # --- Get basic track info (name, album, cover, etc.) ---
    track_res = requests.get(f"https://api.spotify.com/v1/tracks/{song_id}", headers=headers)
    if track_res.status_code != 200:
        return jsonify({"error": "Failed to fetch track data"}), track_res.status_code
    track = track_res.json()

    # --- Get audio features (BPM, energy, etc.) ---
    features_res = requests.get(f"https://api.spotify.com/v1/audio-features/{song_id}", headers=headers)
    if features_res.status_code != 200:
        features = {}
    else:
        features = features_res.json()

    # --- Merge the two sets of data ---
    song_data = {
        "id": track["id"],
        "name": track["name"],
        "album_cover": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
        "duration_ms": track["duration_ms"],

        # Audio features
        "bpm": round(features.get("tempo", 0), 2) if features else None,
        "energy": features.get("energy") if features else None
    }

    return jsonify(song_data)

if __name__ == "__main__":
    app.run(debug=True)
