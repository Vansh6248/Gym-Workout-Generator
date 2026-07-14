<<<<<<< HEAD
print("Hello")
=======
import random 
import sqlite3


# Introduction
print("Welcome to the workout creator app.")

print("This app will ask you a few questions to determine your goals and preferences, and create a personalised workout and a calorie goal to help you achieve your goals.")

print("Firstly, we need to calculate your daily calorie intake. I will ask you a few questions about your current exercise habits and condition.")

# Ask questions to determine caloric maintenance
weight = int(input("Enter your weight in kg: "))
age = int(input("Enter your age: "))
height = int(input("Enter your height in cm: "))
sex = int(input("Please enter your sex. Enter 1 for female and 2 for male: "))

print("Enter your activity level.")
print("1 = Sedentary")
print("2 = Lightly active (1-3 days/week)")
print("3 = Moderately active (3-5 days/week)")
print("4 = Very active (6-7 days/week)")
print("5 = Extremely active (7 days/week or physical job)")

activity_level = int(input("Enter activity level here: "))

#Validate User Inputs
# Simple validation and BMR calculation
def validate_user_input():  
    if weight <= 0 or age <= 0 or height < 100 or activity_level < 1 or activity_level > 5:
        print("Weight, age, height or activity level is not valid, please try again.")
        quit()

validate_user_input() 

if sex == 1:
    BMR = 10 * weight + 6.25 * height - 5 * age - 161
elif sex == 2:
    BMR = 10 * weight + 6.25 * height - 5 * age + 5


# Daily calorie maintenance calculator
if activity_level == 1:
    daily_caloric_intake = BMR * 1.2
elif activity_level == 2:
    daily_caloric_intake = BMR * 1.375
elif activity_level == 3:
    daily_caloric_intake = BMR * 1.55
elif activity_level == 4:
    daily_caloric_intake = BMR * 1.725
elif activity_level == 5:
    daily_caloric_intake = BMR * 1.9

print(f"Your estimated daily calorie maintenance is {daily_caloric_intake:.0f} calories.")

# Ask the user questions about their goals and preferences
print("Now I will ask you a few questions about your goals and preferences for your workouts.")

goal = int(input("Enter 1 if you want to lose weight, or 2 if you want to gain muscle: "))
days_per_week = int(input("Enter how many workouts you want to do in a week (1-7): "))
workout_length = int(input("How long in minutes do you want each workout to be? Enter in a multiple of 8: "))
experience_level = int(input("Enter 1 if you are completely new to resistance training, or 2 if you are experienced: "))

if workout_length < 24: 
    print("It is not advised for a workout to be this short, are you sure you want to continue? ")
elif workout_length > 64: 
    print("It is not advised for a workout to be this long, are you sure you want to continue? ")





>>>>>>> 53d6328f035e5b5528918d8c58a3c0ed8caba712
