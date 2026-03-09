from flask import Flask, render_template, request, redirect, url_for, session, flash

import json, os

app = Flask(__name__)
app.secret_key = ("supersecretkey")
DATA_FILE = "data/users.json"


# Utility function to read/write users
def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/education")
def education():
    return render_template("education.html")


@app.route("/zoo_booking", methods=["GET", "POST"])
def zoo_booking():
    if request.method == "POST":
        flash("Zoo ticket booked successfully", "success")
        return redirect(url_for("zoo_booking"))
    return render_template("zoo_booking.html")


@app.route("/hotel_booking", methods=["GET", "POST"])
def hotel_booking():
    if request.method == "POST":
        flash("Hotel booking submitted", "success")
        return redirect(url_for("hotel_booking"))
    return render_template("hotel_booking.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users = load_users()
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            flash("Username already exists", "danger")
        else:
            users[username] = {"password": password, "rewards": 0}
            save_users(users)
            flash("Registration successful Please log in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_users()
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            session["user"] = username
            flash("Logged in successfully", "success")
            return redirect(url_for("profile"))
        else:
            flash("Invalid credentials beans level 100", "danger")
    return render_template("login.html")


@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))

    users = load_users()
    user_data = users[session["user"]]
    return render_template("profile.html", username=session["user"], rewards=user_data["rewards"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)