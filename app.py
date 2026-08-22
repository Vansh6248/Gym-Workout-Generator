import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from workout_generator import generate_workout
from calorie_calculator import calculate_calories
from auth import setup_auth
from auth import change_username as change_username_from_auth

app = Flask(__name__)
app.secret_key = "your-secret-key-change-this"
setup_auth(app)


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


@app.route("/change-username", methods=["GET", "POST"])
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
