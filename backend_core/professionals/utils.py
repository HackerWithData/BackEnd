import json

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from .models import PROFESSIONAL_CHOICES, Professional, DataCollection


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


def get_professional(id=None):
    if not id:
        return None
    try:
        professional = Professional.objects.get(id=id)
        return professional
    except Professional.DoesNotExist:
        return None


def create_professional(**data):
    if isinstance(data.get('phone', None), dict):
        phone = json.dumps(data.get('phone', ''))
        data.update({'phone': phone})
    Professional.objects.create(**data)


def create_data_collection(professional=None, pro_info=None):
    if not isinstance(pro_info, dict):
        return
    try:
        data_collection = DataCollection.objects.get(professional=professional)
        professional_info = json.loads(data_collection.professional_info)
        professional_info.update(pro_info)
        data_collection.professional_info = json.dumps(professional_info)
        data_collection.save()
    except DataCollection.DoesNotExist:
        pro_info = json.dumps(pro_info)
        DataCollection.objects.create(professional=professional, professional_info=pro_info)


def get_professional_info(professional):
    try:
        pro_info = DataCollection.objects.get(professional=professional).professional_info
    except DataCollection.DoesNotExist:
        return None
    pro_info = json.loads(pro_info)
    ret = {}
    for db_source in pro_info.keys():
        source = ContentType.objects.get(model=db_source).model_class()
        id = pro_info[db_source]
        try:
            info = source.objects.get(id=id)
            ret.update({db_source: info})
        except ObjectDoesNotExist:
            pass
    return ret

