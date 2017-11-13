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

#TODO: need to change in the future
def get_state_full_name(state):
    FullName = "California"
    return FullName


def avg_rating(review, rt):
    s = 0
    l = 0
    if review:
        for r in review:
            rate_list = [i.rating_score for i in r.userrating_set.all() if i.rating_type == rt]
            s += sum(rate_list)
            l += len(rate_list)
        return s * 1.0 / l
    else:
        return 0