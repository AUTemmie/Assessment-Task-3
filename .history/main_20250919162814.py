from flask import Flask
from flask import render_template
from flask import request
import database_manager as dbHandler
from flask import redirect


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@app.route("/index.html", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/friends")
def friends():
    return render_template("friends.html")


@app.route("/tasks")
def tasks():
    return render_template("task.html")


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

        if username == "admin" and password == "richardisastupidpoo":
            return redirect("/")
        else:
            error = "Invalid username or password"
            # pass hide_layout=True
            return render_template("Login.html", error=error, hide_layout=True)

    # GET request
    return render_template("Login.html", hide_layout=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
