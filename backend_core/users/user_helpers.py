from contractors.models import Contractor
from designers.models import Designer
from architects.models import Architect
from meisters.models import Meister
from django.core.exceptions import ObjectDoesNotExist
from professionals.models import Professional
from professionals.utils import CONTRACTOR, ARCHITECT, DESIGNER, MEISTER


def get_professional_user(user):
    professional_profile = user.professional_profiles.first()
    professional = professional_profile.professional
    return professional


def get_professional_corresponding_object_by_type_and_lic(prof_type, lic):
    if prof_type == CONTRACTOR:
        ret_professional_object = Contractor.objects.get(lic_num=lic)
    elif prof_type == ARCHITECT:
        ret_professional_object = Architect.objects.get(lic_num=lic)
    elif prof_type == DESIGNER:
        ret_professional_object = Designer.objects.get(lic_num=lic)
    else:
        raise UndefinedType("Error: Undefined Type in Object")
    return ret_professional_object


def get_professional_corresponding_object_by_user(user):
    professional_profile = user.professional_profiles.first()
    professional = professional_profile.professional
    prof_type = professional.type
    if prof_type == CONTRACTOR:
        ret_professional_object = Contractor.objects.get(lic_num=professional.lic_num)
    elif prof_type == ARCHITECT:
        ret_professional_object = Architect.objects.get(lic_num=professional.lic_num)
    elif prof_type == DESIGNER:
        ret_professional_object = Designer.objects.get(lic_num=professional.lic_num)
    else:
        raise UndefinedType("Error: Undefined Type in Object")
    return ret_professional_object


def get_professional_and_professional_corresponding_object_by_user(user):
    professional_profile = user.professional_profiles.first()
    professional = professional_profile.professional
    ret_professional = professional
    prof_type = professional.type
    if prof_type == CONTRACTOR:
        ret_professional_object = Contractor.objects.get(lic_num=professional.lic_num)
    elif prof_type == ARCHITECT:
        ret_professional_object = Architect.objects.get(lic_num=professional.lic_num)
    elif prof_type == DESIGNER:
        ret_professional_object = Designer.objects.get(lic_num=professional.lic_num)
    elif prof_type == MEISTER:
        ret_professional_object = Meister.objects.get(lic_num=professional.lic_num)
    else:
        raise UndefinedType("Error: Undefined Type in Object")
    return ret_professional, ret_professional_object


def create_professional_corresponding_object(prof_type, lic):
    if prof_type == CONTRACTOR:
        ret_professional_object = Contractor.objects.create(lic_num=lic)
    elif prof_type == ARCHITECT:
        ret_professional_object = Architect.objects.create(lic_num=lic)
    elif prof_type == DESIGNER:
        ret_professional_object = Designer.objects.create(lic_num=lic)
    else:
        raise UndefinedType("Error: Undefined Type in Object")
    return ret_professional_object


def retrieve_professional_info(request):
    prof_type = request.GET['type'].upper()
    lic = request.GET['lic']
    try:
        professional = Professional.objects.get(lic_num=lic, type=prof_type)
        professional_types = professional.professional_types.all()
        subtypes = [professional_type.subtype for professional_type in professional_types]
    except ObjectDoesNotExist:
        return None

    # retrieve corresponding professional through different table
    ret_professional_object = get_professional_corresponding_object_by_type_and_lic(prof_type=prof_type, lic=lic)

    ret = {
        'name': professional.name,
        'entity_type': professional.entity_type,
        'subtype': subtypes,
        'state': professional.state,
        'postal_code': professional.postal_code,
        'street_address': ret_professional_object.street_address
    }

    return ret


class UndefinedType(Exception):
    pass
