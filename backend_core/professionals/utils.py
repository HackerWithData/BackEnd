from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist


from professionals.models import (
    PROFESSIONAL_CHOICES,
    Professional,
    DataCollection,
    ProfessionalType,
    CONTRACTOR,
)
from projects.utils import get_a_uuid

# TODO: need to change in the future
def get_state_full_name(state):
    FullName = "California"
    return FullName


def check_professional_type(request):
    return 'professional'


def get_professionals(by_datacollection=False, *args, **kwargs):
    if by_datacollection:
        records = DataCollection.objects.filter(*args, **kwargs)
        return list({record.professional for record in records})
    return Professional.objects.filter(*args, **kwargs).distinct()


def get_professional(uuid=None, id=None):
    if not uuid and not id:
        return None
    if uuid:
        try:
            professional = Professional.objects.get(uuid=uuid)
            return professional
        except Professional.DoesNotExist:
            return None
    elif id:
        try:
            professional = Professional.objects.get(id=id)
            return professional
        except Professional.DoesNotExist:
            return None


def create_professional(**data):
    professional_uuid = get_a_uuid(*['professional'])
    data.update({'uuid': professional_uuid})
    professional = Professional.objects.create(**data)
    return professional


def get_or_create_professional(**data):
    professional, created = Professional.objects.get_or_create(**data)
    if created:
        professional.save()
    else:
        professional.uuid = get_a_uuid(*['professional'])
        professional.save()
    return professional


def update_professional(uuid=None, professional=None, **data):
    if not uuid and not professional:
        return
    if not professional:
        professional = get_professional(uuid=uuid)
    for attr_name, attr_val in data.items():
        setattr(professional, attr_name, attr_val)
    professional.save()
    return professional


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


def create_professional_type(professional, professional_type, professional_subtypes):
    professionaltypes = ProfessionalType.objects.filter(professional_id=professional.id)
    types = [pt.type for pt in professionaltypes]
    subtypes = [pt.subtype for pt in professionaltypes]
    for t in professional_type:
        if t != CONTRACTOR and t not in types:
            ProfessionalType.objects.create(
                professional=professional,
                type=t,
                subtype=t,
            )
        elif t == CONTRACTOR:
            for subtype in professional_subtypes:
                if subtype not in subtypes:
                    ProfessionalType.objects.create(
                        professional=professional,
                        type=t,
                        subtype=subtype
                    )
