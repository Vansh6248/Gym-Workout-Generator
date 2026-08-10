def calculate_bmr(weight, height, age, sex):
    if sex == "male":
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        return (10 * weight) + (6.25 * height) - (5 * age) - 161


def calculate_calories(weight, height, age, sex, activity_level):
    bmr = calculate_bmr(weight, height, age, sex)

    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
        "extra_active": 2.0
    }

    multiplier = activity_multipliers.get(activity_level, 1.2)

    calories = bmr * multiplier

    return round(calories)