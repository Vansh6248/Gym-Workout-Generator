import sqlite3

#======================== USED AI TO POPULATE DATABASE ========================#

# Connect to the database
conn = sqlite3.connect("exercise_database.db")
cursor = conn.cursor()

# Delete the table if it already exists
cursor.execute("DROP TABLE IF EXISTS exercises")

# Create the exercises table
cursor.execute("""
CREATE TABLE exercises (
    id INTEGER PRIMARY KEY,
    exercise_name TEXT NOT NULL,
    level TEXT NOT NULL,
    muscle_group TEXT NOT NULL
)
""")

# Exercises
exercises = [

    # Chest
    (1, "Barbell Bench Press", "Beginner", "Chest"),
    (2, "Incline Dumbbell Press", "Beginner", "Chest"),
    (3, "Machine Chest Press", "Beginner", "Chest"),

    # Back
    (4, "Lat Pulldown", "Beginner", "Back"),
    (5, "Seated Cable Row", "Beginner", "Back"),
    (6, "Pull-Up", "Experienced", "Back"),
    (7, "Barbell Row", "Experienced", "Back"),

    # Shoulders
    (8, "Overhead Press", "Beginner", "Shoulders"),
    (9, "Dumbbell Shoulder Press", "Beginner", "Shoulders"),
    (10, "Lateral Raise", "Beginner", "Shoulders"),

    # Biceps
    (11, "Barbell Curl", "Beginner", "Biceps"),
    (12, "Hammer Curl", "Beginner", "Biceps"),
    (13, "Preacher Curl", "Experienced", "Biceps"),

    # Triceps
    (14, "Cable Tricep Pushdown", "Beginner", "Triceps"),
    (15, "Overhead Tricep Extension", "Beginner", "Triceps"),
    (16, "Close Grip Bench Press", "Experienced", "Triceps"),

    # Quads
    (17, "Back Squat", "Beginner", "Quads"),
    (18, "Leg Press", "Beginner", "Quads"),
    (19, "Leg Extension", "Beginner", "Quads"),

    # Hamstrings
    (20, "Romanian Deadlift", "Experienced", "Hamstrings"),
    (21, "Lying Leg Curl", "Beginner", "Hamstrings"),

    # Glutes
    (22, "Barbell Hip Thrust", "Beginner", "Glutes"),

    # Calves
    (23, "Standing Calf Raise", "Beginner", "Calves"),

    # Core
    (24, "Cable Crunch", "Beginner", "Core"),
    (25, "Hanging Leg Raise", "Experienced", "Core"),
]

# Insert exercises
cursor.executemany("""
INSERT INTO exercises (id, exercise_name, level, muscle_group)
VALUES (?, ?, ?, ?)
""", exercises)

# Save changes
conn.commit()

print(f"Successfully inserted {len(exercises)} exercises into exercise_database.db")

# Close the connection
conn.close()