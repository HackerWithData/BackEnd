from contractors.models import Contractor
from designers.models import Designer
from architects.models import Architect
from django.core.exceptions import ObjectDoesNotExist
from professionals.models import Professional
from professionals.utils import CONTRACTOR, ARCHITECT, DESIGNER


def retrieveProfessionalInfo(request):
    prof_type = request.GET['type'].upper()
    lic = request.GET['lic']
    try:
        professional = Professional.objects.get(lic_num=lic, type=prof_type)
    except ObjectDoesNotExist:
        return None
    # retrieve corresponding professional through different table
    if prof_type == CONTRACTOR:
        ret_professinal_object = Contractor.objects.filter(lic_num=lic)
    elif prof_type == ARCHITECT:
        ret_professinal_object = Architect.objects.filter(lic_num=lic)
    elif prof_type == DESIGNER:
        ret_professinal_object = Designer.objects.filter(lic_num=lic)
    else:
        raise UndefinedType("Error: Undefined Type in Object")

    ret = {
        'name': professional.name,
        'entity_type': professional.entity_type,
        'subtype': professional.subtype,
        'state': professional.state,
        'postal_code': professional.postal_code,
        'street_address': ret_professinal_object.street_address
    }

    return ret


class UndefinedType(Exception):
    pass
