from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from .models import PROFESSIONAL_CHOICES, Professional


def check_professional_type(request):
    for i in [j[0] for j in PROFESSIONAL_CHOICES]:
        if i.lower() in request.path:
            model_type = i.lower()
            return model_type
        else:
            pass


def get_professional_instance(model_type=None, lic_num=None):
    if not model_type or not lic_num:
        return None
    try:
        model = ContentType.objects.get(model=model_type).model_class()
        instance = model.objects.get(lic_num=lic_num)
        return instance
    except ObjectDoesNotExist:
        return None


def get_professionals(*args, **kwargs):
    return Professional.objects.filter(*args, **kwargs).distinct()

