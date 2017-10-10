def convert_hscore_to_rank(hscore):
    percentage = round(hscore.rank * 100.0 / hscore.max, 2)
    if percentage > 75:
        letter_grade = "A+++"
    elif percentage > 70:
        letter_grade = "A++"
    elif percentage > 65:
        letter_grade = "A+"
    elif percentage > 60:
        letter_grade = "A"
    elif hscore.score == 0:
        letter_grade = "Warning"
    else:
        letter_grade = 'A-'
    return letter_grade
