from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _,  ugettext_lazy as _

from .models import Hscore


def get_hscore(contractor_id):
    try:
        hscore = Hscore.objects.get(contractor_id=contractor_id)
    except:
        hscore = Hscore.objects.create(contractor=contractor, score=None, rank=None, max=None)
    return hscore