import sqlite3

db = sqlite3.connect("database.db")
cursor = db.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        experience_level INTEGER NOT NULL,
        muscle_group TEXT NOT NULL
    )
"""
)

exercises = [
    ("Barbell Back Squat", 2, "Quads"),
    ("Barbell Front Squat", 2, "Quads"),
    ("Leg Press", 1, "Quads"),
    ("Goblet Squat", 1, "Quads"),
    ("Bulgarian Split Squat", 2, "Quads"),
    ("Leg Extensions", 1, "Quads"),
    ("Dumbbell Lunge", 1, "Quads"),
    ("Hack Squat", 2, "Quads"),
    ("Box Squat", 1, "Quads"),
    ("Smith Machine Squat", 1, "Quads"),
    ("Romanian Deadlift", 2, "Hamstrings"),
    ("Lying Leg Curl", 1, "Hamstrings"),
    ("Seated Leg Curl", 1, "Hamstrings"),
    ("Glute-Ham Raise", 2, "Hamstrings"),
    ("Dumbbell Romanian Deadlift", 1, "Hamstrings"),
    ("Barbell Good Morning", 2, "Hamstrings"),
    ("Single-Leg Romanian Deadlift", 2, "Hamstrings"),
    ("Kettlebell Swing", 1, "Hamstrings"),
    ("Sumo Deadlift", 2, "Hamstrings"),
    ("Deficit Deadlift", 2, "Hamstrings"),
    ("Barbell Hip Thrust", 1, "Glutes"),
    ("Cable Pull-Through", 1, "Glutes"),
    ("Dumbbell Glute Bridge", 1, "Glutes"),
    ("Frog Pumps", 1, "Glutes"),
    ("Deficit Reverse Lunge", 2, "Glutes"),
    ("Curtsy Lunge", 1, "Glutes"),
    ("Abductor Machine", 1, "Glutes"),
    ("Cable Kickbacks", 1, "Glutes"),
    ("Standing Calf Raise", 1, "Calves"),
    ("Seated Calf Raise", 1, "Calves"),
    ("Leg Press Calf Raise", 1, "Calves"),
    ("Donkey Calf Raise", 1, "Calves"),
    ("Barbell Bench Press", 1, "Chest"),
    ("Dumbbell Bench Press", 1, "Chest"),
    ("Incline Barbell Bench Press", 2, "Chest"),
    ("Incline Dumbbell Bench Press", 1, "Chest"),
    ("Decline Barbell Bench Press", 2, "Chest"),
    ("Chest Fly Machine", 1, "Chest"),
    ("Incline Cable Fly", 2, "Chest"),
    ("Cable Crossover", 2, "Chest"),
    ("Weighted Push-Up", 2, "Chest"),
    ("Chest Dips", 2, "Chest"),
    ("Close-Grip Bench Press", 2, "Chest"),
    ("Floor Press", 1, "Chest"),
    ("Barbell Conventional Deadlift", 2, "Back"),
    ("Barbell Row", 2, "Back"),
    ("One-Arm Dumbbell Row", 1, "Back"),
    ("Lat Pulldown", 1, "Back"),
    ("Seated Cable Row", 1, "Back"),
    ("T-Bar Row", 2, "Back"),
    ("Chest-Supported Row", 1, "Back"),
    ("Weighted Pull-Up", 2, "Back"),
    ("Chin-Up", 1, "Back"),
    ("Inverted Row", 1, "Back"),
    ("Meadows Row", 2, "Back"),
    ("Rack Pull", 2, "Back"),
    ("Straight-Arm Lat Pulldown", 1, "Back"),
    ("Hyperextension", 1, "Back"),
    ("Overhead Press", 2, "Shoulders"),
    ("Seated Dumbbell Shoulder Press", 1, "Shoulders"),
    ("Dumbbell Lateral Raise", 1, "Shoulders"),
    ("Cable Lateral Raise", 1, "Shoulders"),
    ("Dumbbell Rear Delt Fly", 1, "Shoulders"),
    ("Face Pull", 1, "Shoulders"),
    ("Barbell Shrug", 1, "Shoulders"),
    ("Dumbbell Shrug", 1, "Shoulders"),
    ("Push Press", 2, "Shoulders"),
    ("Front Dumbbell Raise", 1, "Shoulders"),
    ("Triceps Rope Pushdown", 1, "Triceps"),
    ("Skull Crusher", 2, "Triceps"),
    ("Overhead Dumbbell Extension", 1, "Triceps"),
    ("Triceps Dips", 1, "Triceps"),
    ("Close-Grip Push-Up", 1, "Triceps"),
    ("Cable Overhead Extension", 1, "Triceps"),
    ("Triceps Kickback", 1, "Triceps"),
    ("Diamond Push-Up", 2, "Triceps"),
    ("JM Press", 2, "Triceps"),
    ("Barbell Bicep Curl", 1, "Biceps"),
    ("Dumbbell Alternate Curl", 1, "Biceps"),
    ("Hammer Curl", 1, "Biceps"),
    ("Incline Dumbbell Curl", 2, "Biceps"),
    ("Preacher Curl", 1, "Biceps"),
    ("Concentration Curl", 1, "Biceps"),
    ("Cable Bicep Curl", 1, "Biceps"),
    ("Spider Curl", 2, "Biceps"),
    ("Zottman Curl", 2, "Biceps"),
    ("Reverse Barbell Curl", 1, "Biceps"),
    ("Barbell Wrist Curl", 1, "Forearms"),
    ("Behind-the-Back Wrist Curl", 1, "Forearms"),
    ("Farmer's Walk", 1, "Forearms"),
    ("Ab Wheel Rollout", 2, "Abs"),
    ("Hanging Knee Raise", 1, "Abs"),
    ("Hanging Leg Raise", 2, "Abs"),
    ("Weighted Crunch", 1, "Abs"),
    ("Cable Crunch", 1, "Abs"),
    ("Weighted Russian Twist", 1, "Abs"),
    ("Pallof Press", 1, "Abs"),
]

cursor.executemany(
    """
    INSERT INTO exercises (name, experience_level, muscle_group)
    VALUES (?, ?, ?)
""",
    exercises,
)

db.commit()
db.close()

print(f"Done. Added {len(exercises)} items to the database.")
