import hashlib
import os
import sqlite3
from flask import render_template, request, redirect, url_for, session, g


def setup_auth(app):
    """Set up authentication routes for the app."""

    @app.before_request
    def load_user():
        g.user = None
        if "user_id" in session:
            g.user = {"id": session["user_id"], "username": session["username"]}

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            confirm_password = request.form["confirm_password"]

            if password != confirm_password:
                return render_template("signup.html", error="Passwords do not match.")

            conn = sqlite3.connect("accounts.db")
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                conn.close()
                return render_template("signup.html", error="Username already taken.")

            password_hash = hash_password(password)
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                           (username, password_hash))
            conn.commit()
            conn.close()

            return render_template("login.html", success="Account created! Please log in.")

        return render_template("signup.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            conn = sqlite3.connect("accounts.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?",
                           (username,))
            user = cursor.fetchone()
            conn.close()

            if user and verify_password(password, user[2]):
                session["user_id"] = user[0]
                session["username"] = user[1]
                return redirect(url_for("home"))
            else:
                return render_template("login.html", error="Invalid username or password.")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))


def hash_password(password):
    """Hash a password using pbkdf2_hmac."""
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return salt.hex() + password_hash.hex()


def verify_password(password, stored_hash):
    """Verify a password against a stored hash."""
    try:
        salt = bytes.fromhex(stored_hash[:32])
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return password_hash.hex() == stored_hash[32:]
    except Exception:
        return False


def change_username(conn, current_username, new_username, current_password):
    """Change a user's username."""
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?",
                   (current_username,))
    user = cursor.fetchone()

    if not user:
        return (False, "Current username not found.")

    if not verify_password(current_password, user[2]):
        return (False, "Incorrect password.")

    cursor.execute("SELECT id FROM users WHERE username = ?", (new_username,))
    if cursor.fetchone():
        return (False, "That username is already taken.")

    cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user[0]))
    conn.commit()

    return (True, None)
