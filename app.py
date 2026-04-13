import sqlite3
from flask import Flask, render_template, g, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import init_db, get_db, create_user, get_user_by_email

app = Flask(__name__)
# TODO: replace with os.environ.get("SECRET_KEY") before going to production
app.secret_key = "dev-secret-key"

with app.app_context():
    init_db()


@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username         = request.form.get("username", "").strip()
    email            = request.form.get("email", "").strip()
    password         = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not username or not email or not password or not confirm_password:
        return render_template("register.html", error="All fields are required.")

    if len(password) < 8:
        return render_template("register.html",
                               error="Password must be at least 8 characters.")

    if password != confirm_password:
        return render_template("register.html",
                               error="Passwords do not match.")

    try:
        create_user(username, email, generate_password_hash(password))
    except sqlite3.IntegrityError:
        return render_template("register.html",
                               error="Username or email is already registered.")

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("login.html", error="All fields are required.")

    user = get_user_by_email(email)

    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.")

    session["user_id"]  = user["id"]
    session["username"] = user["username"]
    return redirect(url_for("landing"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
