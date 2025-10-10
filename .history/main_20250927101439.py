from flask import Flask, render_template, request, redirect, session
import database_manager as dbHandler

app = Flask(__name__)
db = dbHandler.DBManager()  # create an instance
app.secret_key = "your-secret-key"


@app.route("/", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def index():
    if "user_id" not in session:
        return redirect("/Login")

    user = db.get_user_by_id(
        session["user_id"]
    )  # <-- you need this function in DBManager
    first_name = user["first_name"]
    last_name = user["last_name"]

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

        user = db.get_user_by_first_name(
            username
        )  # <-- consider using get_user_by_username/email instead

        if user:
            if password == user["password"]:
                session["user_id"] = user["id"]  # store ID in session
                return redirect("/")
            else:
                error = "Incorrect password"
        else:
            error = "Username not found"

        return render_template("Login.html", error=error, hide_layout=True)

    return render_template("Login.html", hide_layout=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
