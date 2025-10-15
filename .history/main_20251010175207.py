from flask import Flask, render_template, request, redirect, session, url_for
import database_manager as dbHandler
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your-secret-key"  # required for sessions

# Initialize database manager
db = dbHandler.DBManager()

# 🔧 Ensure messages table exists on startup
db._create_messages_table()


# 🏠 HOME PAGE
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


# 💬 CHAT PAGE
@app.route("/chat", methods=["GET"])
def chat():
    if "username" not in session:
        return redirect("/Login")

    messages = db.get_messages()
    return render_template("chat.html", messages=messages)


# 📤 SEND MESSAGE
@app.route("/send_message", methods=["POST"])
def send_message():
    if "username" not in session:
        return redirect("/Login")

    sender = session["username"]
    text = request.form["message"]
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.add_message(sender, text, time)
    return redirect(url_for("chat"))


# 👥 FRIENDS PAGE
@app.route("/friends")
def friends():
    if "username" not in session:
        return redirect("/Login")
    return render_template("friends.html")


# 📚 RESOURCES PAGE
@app.route("/resources")
def resources():
    if "username" not in session:
        return redirect("/Login")
    return render_template("resource.html")


# ⚙️ SETTINGS PAGE
@app.route("/settings")
def settings():
    if "username" not in session:
        return redirect("/Login")
    return render_template("settings.html")


# 🔑 LOGIN PAGE
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


# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/Login")


# 🧠 Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
