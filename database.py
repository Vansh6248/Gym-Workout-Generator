import sqlite3


#=============== CONNECT TO DATABASE AND CLOSE DATABASE CONNECTION =================#

#Connect to the database
def connect_to_database():
    connection = sqlite3.connect('exercise_database.db')
    cursor = connection.cursor()
    return connection, cursor

# Close the database connection
def close_database_connection(connection):
    connection.close()

#======================== CREATE TABLES ========================#

#Saves user workout (if logged in)
def create_saved_exercises_table():
    connection = sqlite3.connect('exercise_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_name TEXT NOT NULL,
            level TEXT NOT NULL,
            muscle_group TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

#Saves user workout history (if logged in)
def create_workout_history_table():
    connection = sqlite3.connect('exercise_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_name TEXT NOT NULL,
            level TEXT NOT NULL,
            muscle_group TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

#add to workout history (if logged in)
def add_to_workout_history(exercise_name, level, muscle_group, date):
    connection = sqlite3.connect('exercise_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO workout_history (exercise_name, level, muscle_group, date)
        VALUES (?, ?, ?, ?)
    ''', (exercise_name, level, muscle_group, date))
    connection.commit()
    connection.close()

#delete from workout history (if logged in)
def delete_from_workout_history(history_id):
    connection = sqlite3.connect('exercise_database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM workout_history WHERE id = ?', (history_id,))
    connection.commit()
    connection.close()

#get workout history (if logged in)
def get_workout_history():
    connection = sqlite3.connect('exercise_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM workout_history')
    history = cursor.fetchall()
    connection.close()
    return history    


#======================== CRUD OPERATIONS ========================#

#allows user to add exercise (if logged in)
def add_exercise(exercise_name, level, muscle_group):
    connection = sqlite3.connect('exercise_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO saved_exercises (exercise_name, level, muscle_group)
        VALUES (?, ?, ?)
    ''', (exercise_name, level, muscle_group))
    connection.commit()
    connection.close()

#allows user to delete exercise from saved exercises (if logged in)
def delete_exercise(exercise_id):
    connection = sqlite3.connect('exercise_database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM saved_exercises WHERE id = ?', (exercise_id,))
    connection.commit()
    connection.close()

#update exercise (if logged in)
def update_exercise(exercise_id, exercise_name, level, muscle_group):
    connection = sqlite3.connect('exercise_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE saved_exercises
        SET exercise_name = ?, level = ?, muscle_group = ?
        WHERE id = ?
    ''', (exercise_name, level, muscle_group, exercise_id))
    connection.commit()
    connection.close()

#gets all exercises from the database 
def get_all_exercises():
    connection = sqlite3.connect('exercise_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM saved_exercises')
    exercises = cursor.fetchall()
    connection.close()
    return exercises

#get an individual exercise from the database
def get_exercise_by_id(exercise_id):
    connection = sqlite3.connect('exercise_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM saved_exercises WHERE id = ?', (exercise_id,))
    exercise = cursor.fetchone()
    connection.close()
    return exercise