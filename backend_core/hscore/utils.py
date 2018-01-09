from .models import Hscore


def get_hscore(contractor=None, contractor_id=None):
    if not contractor or not contractor_id:
        return None
    try:
        hscore = Hscore.objects.get(contractor_id=contractor_id)
    except Hscore.DoesNotExist:
        hscore = Hscore.objects.create(contractor=contractor, score=None, rank=None, max=None)
    return hscore