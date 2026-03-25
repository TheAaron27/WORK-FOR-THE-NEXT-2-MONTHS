from flask import Flask, render_template, request, redirect, url_for, session, flash

import json, os

app = Flask(__name__)
app.secret_key = "secretkey"
DATA_FILE = "data/users.json"
DATA_FILE2 = "data/partners.json"


def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)


def load_partners():
    if not os.path.exists(DATA_FILE2):
        return {}
    with open(DATA_FILE2, "r") as f:
        return json.load(f)


def save_partners(partners):
    with open(DATA_FILE2, "w") as f:
        json.dump(partners, f, indent=4)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/shopping")
def shopping():
    return render_template("shopping.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users = load_users()
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            flash("This username has already been taken", "danger")
        else:
            users[username] = {"password": password, "rewards": 0}
            save_users(users)
            flash("Registration success, please log in.", "success")
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
            flash("Login successful", "success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful please try again", "danger")
    return render_template("login.html")


@app.route("/partner_register", methods=["GET", "POST"])
def partner_register():
    if request.method == "POST":
        partners = load_partners()
        username = request.form["username"]
        password = request.form["password"]
        farmerID = request.form["farmerID"]

        if username in partners:
            flash("This username has already been taken", "danger")
        else:
            partners[username] = {"password": password,"farmerID": farmerID, "rewards": 0}
            save_partners(partners)
            flash("Registration success, please log in.", "success")
            return redirect(url_for("partner_login"))
    return render_template("partner_register.html")


@app.route("/partner_login", methods=["GET", "POST"])
def partner_login():
    if request.method == "POST":
        partners = load_partners()
        username = request.form["username"]
        password = request.form["password"]
        farmerID = request.form["farmerID"]
        if username in partners and partners[username]["password"] == password:
            session ["partner"] = username
            flash("Login successful", "success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful please try again", "danger")
    return render_template("partner_login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))


@app.route("/partner_logout")
def partner_logout():
    session.pop("partner", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))


@app.route("/partner_profile")
def partner_profile():
    return render_template("partner_profile.html")


@app.route("/partner_stock")
def partner_stock():
    return render_template("partner_stock.html")







if __name__ == "__main__":
    app.run(debug=True)