import sqlite3
from flask import render_template, request, session, redirect, url_for, flash, g
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = "accounts.db"

def setup_auth(app):
    # Runs before every request: makes g.user available in all templates.
    @app.before_request
    def load_logged_in_user():
        g.user = None
        user_id = session.get("user_id")
        if user_id is not None:
            db = sqlite3.connect(DB_PATH)
            db.row_factory = sqlite3.Row
            g.user = db.execute(
                "SELECT * FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            db.close()

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            username = request.form.get("username").strip()
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")

            if password != confirm_password:
                flash("Passwords do not match.", "error")
                return redirect(url_for("signup"))

            db = sqlite3.connect(DB_PATH)

            existing = db.execute(
                "SELECT id FROM users WHERE username = ?", (username,)
            ).fetchone()
            if existing:
                db.close()
                flash("That username is already taken.", "error")
                return redirect(url_for("signup"))

            # Using pbkdf2:sha256 to support Python 3.8
            db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, generate_password_hash(password, method="pbkdf2:sha256")),
            )
            db.commit()
            db.close()
            flash("Account created! You can now log in.")
            return redirect(url_for("login"))

        return render_template("signup.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username").strip()
            password = request.form.get("password")

            db = sqlite3.connect(DB_PATH)
            db.row_factory = sqlite3.Row
            user = db.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchone()
            db.close()

            if user is None or not check_password_hash(user["password_hash"], password):
                flash("Invalid username or password.", "error")
                return redirect(url_for("login"))

            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("home"))

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("You have been logged out.")
        return redirect(url_for("home"))
