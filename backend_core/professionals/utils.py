from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from professionals.models import PROFESSIONAL_CHOICES, Professional, DataCollection
from projects.utils import get_a_uuid


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


def get_professionals(by_datacollection=False, *args, **kwargs):
    if by_datacollection:
        records = DataCollection.objects.filter(*args, **kwargs)
        return list({record.professional for record in records})
    return Professional.objects.filter(*args, **kwargs).distinct()


def get_professional(uuid=None):
    if not uuid:
        return None
    try:
        professional = Professional.objects.get(uuid=uuid)
        return professional
    except Professional.DoesNotExist:
        return None


def create_professional(**data):
    professional_uuid = get_a_uuid(*['professional'])
    data.update({'uuid': professional_uuid})
    Professional.objects.create(**data)


def create_data_collection(professional=None, datasource=None, object_id=None, lic_num=None):
    if not professional or not datasource or not object_id or not lic_num:
        return
    try:
        content_type = ContentType.objects.get(model=datasource)
    except ContentType.DoesNotExist:
        return
    DataCollection.objects.create(
        professional=professional,
        content_type=content_type,
        object_id=object_id,
        lic_num=lic_num,
    )


def get_professional_info(professional):
    ret = {}
    records = DataCollection.objects.filter(professional=professional)
    for record in records:
        try:
            data_source = record.content_type.model_class()
            data = data_source.objects.get(id=record.object_id)
            ret.update({record.content_type.model: data})
        except ObjectDoesNotExist:
            pass
    return ret
