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
    last_name = user.get("last_name", "")  # default empty if missing

    return render_template("index.html", first_name=first_name, last_name=last_name)


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/friends")
def friends():
    return render_template("friends.html")


@app.route("/resources")
def resources():
    return render_template("resource.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/Login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = db.get_user_by_first_name(username)

        if user:
            if password == user["password"]:
                # Store the first_name in session
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
