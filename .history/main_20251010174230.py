from flask import Flask, render_template, request, redirect, session, url_for
import database_manager as dbHandler
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your-secret-key"  # needed for sessions

db = dbHandler.DBManager()  # create an instance


@app.route("/", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def index():
    if "username" not in session:
        return redirect("/Login")

    user = db.get_user_by_first_name(session["username"])
    if not user:  # failsafe in case user not found
        return redirect("/Login")

    first_name = user["first_name"]
    last_name = user.get("last_name", "")  # optional

    return render_template("index.html", first_name=first_name, last_name=last_name)


# 🟩 CHAT PAGE (WITH DATABASE INTEGRATION)
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "username" not in session:
        return redirect("/Login")

    if request.method == "POST":
        message_text = request.form["message"]
        sender = session["username"]
        time_str = datetime.now().strftime("%I:%M %p")
        db.add_message(sender, message_text, time_str)
        return redirect(url_for("chat"))

    # Fetch and format messages
    rows = db.get_messages()
    messages = []
    for sender, text, time in rows:
        msg_type = "sent" if sender == session["username"] else "received"
        messages.append({"text": text, "type": msg_type, "time": time})

    return render_template("chat.html", messages=messages)


@app.route("/friends")
def friends():
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
