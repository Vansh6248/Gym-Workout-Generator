import sqlite3 
import random
DATABASE = "exercise_database.db"

def get_exercises(goal, experience): conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if goal == "lose_weight":
        database_goal = "Weight Loss"
    else:
        database_goal = "Muscle Building"
    if experience == "beginner_intermediate":
        cursor.execute(
            "SELECT * FROM exercises WHERE training_goal = ? AND level = ?",
            (database_goal, "Beginner")
        )
    else:
        cursor.execute(
            "SELECT * FROM exercises WHERE training_goal = ?",
            (database_goal,)
        )
    exercises = cursor.fetchall()
    conn.close()
    return exercises

def get_cardio(): conn = sqlite3.connect(DATABASE) cursor =
conn.cursor()
    cursor.execute(
        "SELECT * FROM exercises WHERE training_goal = ? ORDER BY RANDOM() LIMIT 1",
        ("Weight Loss",)
    )
    exercise = cursor.fetchone()
    conn.close()
    return exercise

def choose_split(days): splits = { 1: [("Monday", "Full Body")], 2:
[("Monday", "Upper"), ("Thursday", "Lower")], 3: [("Monday", "Push"),
("Wednesday", "Pull"), ("Friday", "Legs")], 4: [("Monday", "Upper"),
("Tuesday", "Lower"), ("Thursday", "Upper"), ("Friday", "Lower")], 5:
[("Monday", "Upper"), ("Tuesday", "Lower"), ("Wednesday", "Push"),
("Friday", "Pull"), ("Saturday", "Legs")], 6: [("Monday", "Push"),
("Tuesday", "Pull"), ("Wednesday", "Legs"), ("Friday", "Push"),
("Saturday", "Pull"), ("Sunday", "Legs")], 7: [("Monday", "Upper"),
("Tuesday", "Lower"), ("Wednesday", "Push"), ("Thursday", "Pull"),
("Friday", "Legs"), ("Saturday", "Upper"), ("Sunday", "Lower")] } return
splits[days]

def get_muscles(split): if split == "Push": return ["Chest",
"Shoulders", "Triceps"] if split == "Pull": return ["Back", "Biceps"] if
split == "Legs": return ["Quads", "Hamstrings", "Glutes", "Calves"] if
split == "Upper": return ["Chest", "Back", "Shoulders", "Biceps",
"Triceps"] if split == "Lower": return ["Quads", "Hamstrings", "Glutes",
"Calves"] return ["Chest", "Back", "Shoulders", "Quads", "Hamstrings"]

def get_exercise_count(length): if length == "short": return 4 if length
== "medium": return 6 return 8

def generate_workout(goal, experience, days, workout_length): exercises
= get_exercises(goal, experience) week = choose_split(days) workout = {}
used = [] count = get_exercise_count(workout_length)
    for day_name, split in week:
        session = []
        muscles = get_muscles(split)
        each = max(1, count // len(muscles))
        for muscle in muscles:
            choices = []
            for exercise in exercises:
                if exercise[3] == muscle and exercise[0] not in used:
                    choices.append(exercise)
            random.shuffle(choices)
            for exercise in choices[:each]:
                used.append(exercise[0])
                session.append((exercise[1], 6))
        if goal == "lose_weight":
            cardio = get_cardio()
            if cardio:
                session.append((cardio[1], cardio[5]))
        workout[day_name] = session
    return workout

def print_workout(workout): for day in workout: print(day) total = 0
        for exercise, minutes in workout[day]:
            print(f"- {exercise} ({minutes} mins)")
            total += minutes
        print(f"Total: {total} mins")
        print()

if __name__ == "__main__":
    workout = generate_workout(goal="gain_muscle", experience="beginner_intermediate", days=4, workout_length="medium")
    print_workout(workout)
