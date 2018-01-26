from .models import Hscore


def get_hscore(contractor=None, contractor_id=None):
    if not contractor or not contractor_id:
        return None
    try:
        hscore = Hscore.objects.get(contractor_id=contractor_id)
    except Hscore.DoesNotExist:
        hscore = Hscore.objects.create(contractor=contractor, score=None, rank=None, max=None)
    return hscore


def convert_hscore_to_rank(hscore=None):
    if not hscore:
        return None
    if hscore.score > 89:
        letter_grade = "A+++"
    elif hscore.score > 80:
        letter_grade = "A++"
    elif hscore.score > 75:
        letter_grade = "A+"
    elif hscore.score > 70:
        letter_grade = "A"
    elif hscore.score == 0:
        letter_grade = _("Warning")
    else:
        letter_grade = 'A-'
    return letter_grade