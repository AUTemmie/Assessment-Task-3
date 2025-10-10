from flask import Flask, render_template, request, redirect
import database_manager as dbHandler

app = Flask(__name__)
db = dbHandler.DBManager()  # create an instance


@app.route("/", methods=["GET", "POST"])
@app.route("/index.html", methods=["GET"])
def index():
    if "first_name" in session:
        return render_template(
            "index.html",
            first_name=session["first_name"],
            last_name=session["last_name"],
        )
    else:
        return redirect("/Login")


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
                return redirect("/")
            else:
                error = "Incorrect password"
        else:
            error = "Username not found"

        return render_template("Login.html", error=error, hide_layout=True)

    return render_template("Login.html", hide_layout=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
