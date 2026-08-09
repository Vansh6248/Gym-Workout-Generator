from flask import Flask, render_template, request
from workout_generator import generate_workout

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    goal = request.form.get("workout_goal")
    experience = request.form.get("experience_level")
    days = int(request.form.get("workout_days"))
    workout_length = request.form.get("workout_length")

    workout = generate_workout(
        goal,
        experience,
        days,
        workout_length
    )
    return render_template("workout.html", workout=workout)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)