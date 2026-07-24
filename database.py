import sqlite3

connection = sqlite3.connect('exercise_database.db')
cursor = connection.cursor()

cursor.execute("SELECT * FROM exercises")

rows = cursor.fetchall()

print(rows)