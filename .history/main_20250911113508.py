from flask import Flask
from flask import render_template
from flask import request
import database_manager as dbHandler

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


@app.route("/Login")
def login():
    return render_template("Login.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
