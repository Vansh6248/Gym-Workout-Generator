import sqlite3

#======================== USED AI TO POPULATE DATABASE

conn = sqlite3.connect("exercise_database.db") 

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS exercises")

cursor.execute(""" CREATE TABLE exercises ( id INTEGER PRIMARY KEY,
exercise_name TEXT NOT NULL, level TEXT NOT NULL, muscle_group TEXT NOT
NULL, training_goal TEXT NOT NULL, duration INTEGER ) """)

exercises = [

    # Chest
    (1, "Barbell Bench Press", "Beginner", "Chest", "Muscle Building", None),
    (2, "Incline Dumbbell Press", "Beginner", "Chest", "Muscle Building", None),
    (3, "Machine Chest Press", "Beginner", "Chest", "Muscle Building", None),

    # Back
    (4, "Lat Pulldown", "Beginner", "Back", "Muscle Building", None),
    (5, "Seated Cable Row", "Beginner", "Back", "Muscle Building", None),
    (6, "Pull-Up", "Experienced", "Back", "Muscle Building", None),
    (7, "Barbell Row", "Experienced", "Back", "Muscle Building", None),

    # Shoulders
    (8, "Overhead Press", "Beginner", "Shoulders", "Muscle Building", None),
    (9, "Dumbbell Shoulder Press", "Beginner", "Shoulders", "Muscle Building", None),
    (10, "Lateral Raise", "Beginner", "Shoulders", "Muscle Building", None),

    # Biceps
    (11, "Barbell Curl", "Beginner", "Biceps", "Muscle Building", None),
    (12, "Hammer Curl", "Beginner", "Biceps", "Muscle Building", None),
    (13, "Preacher Curl", "Experienced", "Biceps", "Muscle Building", None),

    # Triceps
    (14, "Cable Tricep Pushdown", "Beginner", "Triceps", "Muscle Building", None),
    (15, "Overhead Tricep Extension", "Beginner", "Triceps", "Muscle Building", None),
    (16, "Close Grip Bench Press", "Experienced", "Triceps", "Muscle Building", None),

    # Quads
    (17, "Back Squat", "Beginner", "Quads", "Muscle Building", None),
    (18, "Leg Press", "Beginner", "Quads", "Muscle Building", None),
    (19, "Leg Extension", "Beginner", "Quads", "Muscle Building", None),

    # Hamstrings
    (20, "Romanian Deadlift", "Experienced", "Hamstrings", "Muscle Building", None),
    (21, "Lying Leg Curl", "Beginner", "Hamstrings", "Muscle Building", None),

    # Glutes
    (22, "Barbell Hip Thrust", "Beginner", "Glutes", "Muscle Building", None),

    # Calves
    (23, "Standing Calf Raise", "Beginner", "Calves", "Muscle Building", None),

    # Core
    (24, "Cable Crunch", "Beginner", "Core", "Muscle Building", None),
    (25, "Hanging Leg Raise", "Experienced", "Core", "Muscle Building", None),

    # Cardio
    (26, "Exercise Bike", "Beginner", "Cardio", "Weight Loss", 20),
    (27, "Incline Treadmill Walk", "Beginner", "Cardio", "Weight Loss", 30),
    (28, "Rowing Machine", "Beginner", "Cardio", "Weight Loss", 15),
    (29, "Elliptical Trainer", "Beginner", "Cardio", "Weight Loss", 20),
    (30, "Stair Climber", "Beginner", "Cardio", "Weight Loss", 15),

]

cursor.executemany(""" INSERT INTO exercises (id, exercise_name, level,
muscle_group, training_goal, duration) VALUES (?, ?, ?, ?, ?, ?) """,
exercises)

conn.commit()

print(f"Successfully inserted {len(exercises)} exercises into exercise_database.db")

conn.close()
