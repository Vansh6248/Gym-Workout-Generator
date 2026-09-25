import json
import sqlite3
from datetime import datetime


#=============== SAVED WORKOUTS TABLE (logged in users only) =================#

#Create the saved_workouts table in accounts.db if it does not exist
def create_saved_workouts_table():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal TEXT NOT NULL,
            days INTEGER NOT NULL,
            experience TEXT NOT NULL,
            workout_length TEXT NOT NULL,
            workout_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

#Save a workout for a user
def save_workout(conn, user_id, goal, days, experience, workout_length, workout):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO saved_workouts
        (user_id, goal, days, experience, workout_length, workout_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        goal,
        days,
        experience,
        workout_length,
        json.dumps(workout),
        datetime.now().strftime("%d %b %Y at %H:%M")
    ))
    conn.commit()
    return cursor.lastrowid

#Get every saved workout for a user (newest first)
def get_saved_workouts(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, goal, days, experience, workout_length, workout_json, created_at
        FROM saved_workouts
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))
    return cursor.fetchall()

#Get one saved workout for a user (returns None if it is not theirs)
def get_saved_workout_by_id(conn, user_id, workout_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, goal, days, experience, workout_length, workout_json, created_at
        FROM saved_workouts
        WHERE id = ? AND user_id = ?
    """, (workout_id, user_id))
    return cursor.fetchone()

#Update one of the user's saved workouts in place (used when they edit
#a saved workout and hit "Save workout" again)
def update_saved_workout(conn, user_id, workout_id, goal, days, experience, workout_length, workout):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE saved_workouts
        SET goal = ?, days = ?, experience = ?, workout_length = ?, workout_json = ?
        WHERE id = ? AND user_id = ?
    """, (goal, days, experience, workout_length, json.dumps(workout), workout_id, user_id))
    conn.commit()
    return cursor.rowcount > 0

#Delete one of the user's saved workouts (the user_id check stops
#users from deleting each other's workouts)
def delete_saved_workout(conn, user_id, workout_id):
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM saved_workouts WHERE id = ? AND user_id = ?",
        (workout_id, user_id)
    )
    conn.commit()
    return cursor.rowcount > 0


#=============== VALIDATION + LABELS =================#

GOAL_LABELS = {
    "lose_weight": "Lose Weight",
    "gain_muscle": "Gain Muscle"
}

EXPERIENCE_LABELS = {
    "beginner_intermediate": "Beginner",
    "adept": "Adept"
}

LENGTH_LABELS = {
    "short": "Short (30 minutes per session)",
    "medium": "Medium (30-45 minutes per session)",
    "long": "Long (45+ minutes per session)"
}

LOWER_MUSCLES = ["Quads", "Hamstrings", "Glutes", "Calves"]

#Validate the data posted by the "Save workout" button.
#Returns an error message, or None if everything is fine.
def validate_workout_data(goal, days, experience, workout_length, workout):
    if goal not in GOAL_LABELS:
        return "Invalid workout goal."
    try:
        days = int(days)
    except (TypeError, ValueError):
        return "Invalid number of workout days."
    if days < 1 or days > 7:
        return "Invalid number of workout days."
    if experience not in EXPERIENCE_LABELS:
        return "Invalid experience level."
    if workout_length not in LENGTH_LABELS:
        return "Invalid workout length."
    if not isinstance(workout, dict) or not workout:
        return "Invalid workout data."
    return None

#Work out the split name of one session. Uses the same logic as the
#split_short macro on the workout page, so the labels in the saved
#workouts list always match what the user saw when it was generated.
def split_short(session):
    is_lower = False
    has_back = False
    has_chest = False
    has_any = False
    has_lift = False
    exercises = session.get("exercises") or []
    for exercise in exercises:
        if not isinstance(exercise, dict):
            continue
        has_any = True
        if exercise.get("cardio"):
            continue
        has_lift = True
        muscle = exercise.get("muscle", "")
        if muscle in LOWER_MUSCLES:
            is_lower = True
        if muscle in ["Back", "Biceps"]:
            has_back = True
        if muscle == "Chest":
            has_chest = True
    if not has_any:
        return "Workout"
    if not has_lift:
        return "Cardio"
    if is_lower and (has_back or has_chest):
        return "Full Body"
    if is_lower:
        return "Lower"
    if has_back:
        return "Pull"
    if has_chest:
        return "Push"
    return "Workout"

#Build the one-line label shown in the saved workouts list, e.g.
#"Gain Muscle · 6 days/week · Medium (30-45 minutes per session) · Adept · Push/Pull/Lower"
def build_workout_label(goal, days, experience, workout_length, workout):
    parts = []
    if goal in GOAL_LABELS:
        parts.append(GOAL_LABELS[goal])
    try:
        day_count = int(days)
        if day_count == 1:
            parts.append("1 day/week")
        else:
            parts.append(str(day_count) + " days/week")
    except (TypeError, ValueError):
        pass
    if workout_length in LENGTH_LABELS:
        parts.append(LENGTH_LABELS[workout_length])
    if experience in EXPERIENCE_LABELS:
        parts.append(EXPERIENCE_LABELS[experience])
    if isinstance(workout, dict):
        splits = []
        for session in workout.values():
            if not isinstance(session, dict):
                continue
            split = split_short(session)
            if split not in splits:
                splits.append(split)
        if splits:
            parts.append("/".join(splits))
    return " · ".join(parts)