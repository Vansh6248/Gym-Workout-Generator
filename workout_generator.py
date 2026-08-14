import sqlite3
import random

DATABASE = "exercise_database.db"

def get_exercises(goal, experience):
    conn = sqlite3.connect(DATABASE)
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

def get_cardio():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM exercises WHERE training_goal = ? ORDER BY RANDOM() LIMIT 1",
        ("Weight Loss",)
    )
    exercise = cursor.fetchone()
    conn.close()
    return exercise

def choose_split(days):
    splits = {
        1: [("Monday", "Full Body")],
        2: [("Monday", "Upper"), ("Thursday", "Lower")],
        3: [("Monday", "Push"), ("Wednesday", "Pull"), ("Friday", "Legs")],
        4: [("Monday", "Upper"), ("Tuesday", "Lower"), ("Thursday", "Upper"), ("Friday", "Lower")],
        5: [("Monday", "Upper"), ("Tuesday", "Lower"), ("Wednesday", "Push"), ("Friday", "Pull"), ("Saturday", "Legs")],
        6: [("Monday", "Push"), ("Tuesday", "Pull"), ("Wednesday", "Legs"), ("Friday", "Push"), ("Saturday", "Pull"), ("Sunday", "Legs")],
        7: [("Monday", "Upper"), ("Tuesday", "Lower"), ("Wednesday", "Push"), ("Thursday", "Pull"), ("Friday", "Legs"), ("Saturday", "Upper"), ("Sunday", "Lower")]
    }
    # FAILSAFE: never crash on an invalid/missing days value
    try:
        days = int(days)
    except (TypeError, ValueError):
        days = 3
    if days not in splits:
        days = 3
    return splits[days]

def get_muscles(split):
    if split == "Push":
        return ["Chest", "Shoulders", "Triceps"]
    if split == "Pull":
        return ["Back", "Biceps"]
    if split == "Legs":
        return ["Quads", "Hamstrings", "Glutes", "Calves"]
    if split == "Upper":
        return ["Chest", "Back", "Shoulders", "Biceps", "Triceps"]
    if split == "Lower":
        return ["Quads", "Hamstrings", "Glutes", "Calves"]
    return ["Chest", "Back", "Shoulders", "Quads", "Hamstrings"]

def get_exercise_count(length):
    if length == "short":
        return 4
    if length == "medium":
        return 6
    return 8

def generate_workout(goal, experience, days, workout_length):
    if goal == "lose_weight":
        exercises = get_exercises("gain_muscle", experience)
    else:
        exercises = get_exercises(goal, experience)

    # FAILSAFE: empty database -> clear error instead of silent empty workout
    if not exercises:
        raise ValueError("No exercises found in the database for the selected goal/experience level.")

    week = choose_split(days)
    workout = {}

    workout_length = str(workout_length).strip().lower()
    count = get_exercise_count(workout_length)

    if workout_length == "short":
        time_limit = 30
    elif workout_length == "medium":
        time_limit = 45
    else:
        time_limit = 60

    for day_name, split in week:
        session = []
        used = []  # FIX: per-day only, so Friday isn't starved by Tuesday
        muscles = get_muscles(split)
        each = max(2, count // len(muscles))  # FIX: fill toward the top of the range
        current_time = 0

        for muscle in muscles:
            choices = []
            for exercise in exercises:
                if exercise[3] == muscle and exercise[0] not in used:
                    choices.append(exercise)
            random.shuffle(choices)

            muscle_count = 0
            for exercise in choices:
                if len(session) >= count or muscle_count >= each:
                    break

                if muscle in ["Hamstrings", "Calves", "Rear Delts"]:
                    sets = 2
                    reps = "8-12"
                elif muscle in ["Side Delts", "Biceps", "Triceps", "Back"]:
                    sets = 3
                    reps = "8-15"
                else:
                    sets = 3
                    reps = "8-12"

                rest_time = sets
                exercise_time = 6
                total_exercise_time = exercise_time + rest_time

                if current_time + total_exercise_time > time_limit:
                    continue

                used.append(exercise[0])
                session.append({
                    "name": exercise[1],
                    "muscle": exercise[3],
                    "sets": sets,
                    "reps": reps,
                    "minutes": exercise_time,
                    "rest_time": rest_time,
                    "cardio": False
                })
                current_time += total_exercise_time
                muscle_count += 1

        # FAILSAFE: trim to fit, but NEVER leave a day with zero exercises
        while current_time > time_limit and len(session) > 1:
            removed = session.pop()
            current_time -= removed["minutes"] + removed["rest_time"]

        # FAILSAFE: if a day somehow ended up empty, force in one exercise
        if not session:
            for exercise in exercises:
                if exercise[0] not in used:
                    used.append(exercise[0])
                    session.append({
                        "name": exercise[1],
                        "muscle": exercise[3],
                        "sets": 3,
                        "reps": "8-12",
                        "minutes": 6,
                        "rest_time": 3,
                        "cardio": False
                    })
                    current_time = 9
                    break

        if goal == "lose_weight":
            cardio_count = random.randint(1, 2)
            for _ in range(cardio_count):
                cardio = get_cardio()
                if cardio:
                    session.append({
                        "name": cardio[1],
                        "muscle": "Cardio",
                        "sets": None,
                        "reps": None,
                        "minutes": cardio[5],
                        "rest_time": 0,
                        "cardio": True
                    })

            cardio_time = 0
            for exercise in session:
                if exercise["cardio"]:
                    cardio_time += exercise["minutes"]

            workout[day_name] = {
                "exercises": session,
                "total_time": current_time,
                "total_time_with_cardio": current_time + cardio_time
            }
        else:
            workout[day_name] = {
                "exercises": session,
                "total_time": current_time,
                "total_time_with_cardio": current_time
            }

    return workout
