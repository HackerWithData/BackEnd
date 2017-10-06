from contractors.models import Contractor
from designers.models import Designer
from architects.models import Architect
from django.core.exceptions import ObjectDoesNotExist
from professionals.models import Professional
from professionals.utils import CONTRACTOR, ARCHITECT, DESIGNER


def get_professional_corresponding_object(prof_type, lic):
    if prof_type == CONTRACTOR:
        ret_professional_object = Contractor.objects.get(lic_num=lic)
    elif prof_type == ARCHITECT:
        ret_professional_object = Architect.objects.get(lic_num=lic)
    elif prof_type == DESIGNER:
        ret_professional_object = Designer.objects.get(lic_num=lic)
    else:
        raise UndefinedType("Error: Undefined Type in Object")
    return ret_professional_object


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
    print lic
    print prof_type
    try:
        professional = Professional.objects.get(lic_num=lic, type=prof_type)
        professional_types = professional.professional_types.all()
        subtypes = [professional_type.subtype for professional_type in professional_types]
    except ObjectDoesNotExist:
        return None

    # retrieve corresponding professional through different table
    ret_professional_object = get_professional_corresponding_object(prof_type=prof_type, lic=lic)

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
