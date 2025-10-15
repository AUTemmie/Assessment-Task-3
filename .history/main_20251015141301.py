from flask import Flask, render_template, request, redirect, session, url_for
import database_manager as dbHandler
from datetime import datetime
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = "key"


db = dbHandler.DBManager()


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form["first_name"]
        password = request.form["password"]

        # Check if user exists
        existing = db.get_user_by_first_name(first_name)
        if existing:
            return render_template("signup.html", message="Username already exists")

        # Add user
        con = sql.connect(db.dbPath)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO users (first_name, password) VALUES (?, ?)",
            (first_name, password),
        )
        con.commit()
        con.close()

        return redirect(url_for("login"))

    return render_template("signup.html", hide_layout=true)


db._create_messages_table()


@app.context_processor
def inject_notifications():
    friends = [
        {"id": 1, "name": "Rishit Prasad", "description": "Stinking up the room"},
        {
            "id": 2,
            "name": "Sebastion Kameron",
            "description": "Playing plague inc in class",
        },
        {"id": 3, "name": "David Koh", "description": "Working at mcdonalds"},
    ]

    current_time = datetime.now().strftime("%I:%M %p")

    return dict(
        friends=friends,
        current_time=current_time,
    )


@app.route("/", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def index():
    if "username" not in session:
        return redirect("/Login")

    user = db.get_user_by_first_name(session["username"])

    if not user:
        return redirect("/Login")

    first_name = user["first_name"]
    last_name = user.get("last_name", "")

    return render_template("index.html", first_name=first_name, last_name=last_name)


@app.route("/chat", methods=["GET"])
def chat():
    if "username" not in session:
        return redirect("/Login")

    messages = db.get_messages()
    return render_template("chat.html", messages=messages)


@app.route("/send_message", methods=["POST"])
def send_message():
    if "username" not in session:
        return redirect("/Login")

    sender = session["username"]
    text = request.form["message"]
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.add_message(sender, text, time)
    return redirect(url_for("chat"))


@app.route("/friends")
def friends_page():
    if "username" not in session:
        return redirect("/Login")
    return render_template("friends.html")


@app.route("/resources")
def resources():
    if "username" not in session:
        return redirect("/Login")
    return render_template("resource.html")


@app.route("/settings")
def settings():
    if "username" not in session:
        return redirect("/Login")
    return render_template("settings.html")


@app.route("/Login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = db.get_user_by_first_name(username)

        if user:
            if password == user["password"]:
                session["username"] = user["first_name"]
                return redirect("/")
            else:
                error = "Incorrect password"
        else:
            error = "Username not found"

        return render_template("Login.html", error=error, hide_layout=True)

    return render_template("Login.html", hide_layout=True)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/Login")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
