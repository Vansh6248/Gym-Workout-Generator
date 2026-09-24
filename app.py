import os
import json
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from workout_generator import generate_workout
from calorie_calculator import calculate_calories
from auth import setup_auth
from auth import change_username as change_username_from_auth
import saved_workouts

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY is not set")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
csrf = CSRFProtect(app)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[]
)
setup_auth(app, limiter)
saved_workouts.create_saved_workouts_table()


def get_db():
    conn = sqlite3.connect("accounts.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    goal = request.form.get("workout_goal")
    experience = request.form.get("experience_level")
    days = int(request.form.get("workout_days"))
    workout_length = request.form.get("workout_length")
    workout = generate_workout(goal, experience, days, workout_length)
    return render_template(
        "workout.html",
        workout=workout,
        goal=goal,
        experience=experience,
        days=days,
        workout_length=workout_length
    )


@app.route("/calculate-calories", methods=["POST"])
def calculate_calories_route():
    weight = float(request.form.get("weight"))
    height = float(request.form.get("height"))
    age = int(request.form.get("age"))
    sex = request.form.get("sex")
    activity_level = request.form.get("activity_level")
    calories = calculate_calories(weight, height, age, sex, activity_level)
    return {"calories": calories}


# ------------------------------- WORKOUT SAVING ------------------------------- 

@app.route("/save-workout", methods=["POST"])
@limiter.limit("10 per minute")
def save_workout_route():
    if "user_id" not in session:
        return {"success": False, "error": "You must be logged in to save workouts."}, 401

    try:
        data = json.loads(request.form.get("payload", ""))
    except ValueError:
        data = None
    if not isinstance(data, dict):
        return {"success": False, "error": "Invalid workout data."}, 400

    error = saved_workouts.validate_workout_data(
        data.get("goal"),
        data.get("days"),
        data.get("experience"),
        data.get("workout_length"),
        data.get("workout")
    )
    if error:
        return {"success": False, "error": error}, 400

    conn = get_db()
    try:
        saved_workouts.save_workout(
            conn,
            session["user_id"],
            data["goal"],
            int(data["days"]),
            data["experience"],
            data["workout_length"],
            data["workout"]
        )
    finally:
        conn.close()

    return {"success": True}


@app.route("/saved-workouts")
def saved_workouts_page():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    try:
        rows = saved_workouts.get_saved_workouts(conn, session["user_id"])
    finally:
        conn.close()

    workouts = []
    for row in rows:
        try:
            workout = json.loads(row["workout_json"])
        except ValueError:
            workout = None
        workouts.append({
            "id": row["id"],
            "created_at": row["created_at"],
            "label": saved_workouts.build_workout_label(
                row["goal"],
                row["days"],
                row["experience"],
                row["workout_length"],
                workout
            )
        })

    return render_template("saved_workouts.html", workouts=workouts)


@app.route("/delete-saved-workout/<int:workout_id>", methods=["POST"])
@limiter.limit("10 per minute")
def delete_saved_workout_route(workout_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    try:
        saved_workouts.delete_saved_workout(conn, session["user_id"], workout_id)
    finally:
        conn.close()

    return redirect(url_for("saved_workouts_page"))


@app.route("/change-username", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def change_username_page():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        current_username = request.form["current_username"]
        new_username = request.form["new_username"]
        current_password = request.form["current_password"]

        conn = get_db()
        success, error = change_username_from_auth(
            conn, current_username, new_username, current_password
        )
        conn.close()

        if success:
            session["username"] = new_username
            return render_template("change_username.html",
                                   success="Username changed successfully!")
        else:
            return render_template("change_username.html", error=error)

    return render_template("change_username.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)