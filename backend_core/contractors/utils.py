from django.utils.translation import ugettext_lazy as __
def convert_hscore_to_rank(hscore):
    # percentage = round(hscore.rank * 100.0 / hscore.max, 2)
    if hscore > 89:
        letter_grade = "A+++"
    elif hscore > 80:
        letter_grade = "A++"
    elif hscore > 75:
        letter_grade = "A+"
    elif hscore > 70:
        letter_grade = "A"
    elif hscore.score == 0:
        letter_grade = __("Warning")
    else:
        letter_grade = 'A-'
    return letter_grade
