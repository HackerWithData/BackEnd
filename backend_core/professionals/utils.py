from django.contrib.contenttypes.models import ContentType

from .models import PROFESSIONAL_CHOICES, Professional


def check_professional_type(request):
    for i in [j[0] for j in PROFESSIONAL_CHOICES]:
        if i.lower() in request.path:
            model_type = i.lower()
            return model_type
        else:
            pass


def get_professional_instance(model_type, lic_num):
    model = ContentType.objects.get(model=model_type).model_class()
    try:
        instance = model.objects.get(lic_num=lic_num)
        return instance
    except:
        return None


def get_professionals(*args, **kwargs):
    return Professional.objects.filter(*args, **kwargs).distinct()

