from flask import Flask, render_template, request
from workout_generator import generate_workout
from calorie_calculator import calculate_calories
from auth import setup_auth

app = Flask(__name__)
app.secret_key = "put-a-long-random-string-here"

setup_auth(app)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
