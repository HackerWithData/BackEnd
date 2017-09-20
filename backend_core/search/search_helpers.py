import urllib

from contractors.models import Contractor
from designers.models import Designer
from architects.models import Architect
from professionals.models import Professional, ProfessionalType
from professionals.utils import PROFESSIONAL_TYPE_CHOICES, ARCHITECT, DESIGNER, CONTRACTOR


# Ajax POST request
def search_by_address_object(request):
    zipcode = int(request['address']['address_components'][6]['short_name'])
    target = request['target']
    qs_prof = Professional.objects.filter(postal_code=zipcode)
    # TODO: add subtype later
    qs_prof_type = qs_prof.professionaltype_set.filter(type__icontains=target)
    request['target'] =
    return qs_prof_type


# Ajax POST request
def search_by_address_object_redirect_url(request):
    print request
    zipcode = int(request['address']['address_components'][6]['short_name'])
    target = request['target']
    url_parameters = {
        'zipcode': zipcode,
        'target': target
    }
    return urllib.urlencode(url_parameters)


# GET request
def search_by_zipcode(request):
    # TODO: rename target in request and add type
    professional_subtype = request.GET['target']
    professional_type = request.GET['type']
    zipcode = request.GET['zipcode']
    # mediate query set
    qs_prof = Professional.objects.filter(postal_code=zipcode, type=professional_type)
    qs_prof_type = qs_prof.professionaltype_set.filter(subtype=professional_subtype)
    # query set for all qualified professional
    prof_qs = Professional.objects.filter(id__in=qs_prof_type.values('professional_id'))
    # retrieve corresponding professional through different table
    if professional_type.upper() == CONTRACTOR:
        ret_qs = Contractor.objects.filter(lic_num__in=prof_qs.values('lic_num'))
    elif professional_type.upper() == ARCHITECT:
        ret_qs = Architect.objects.filter(lic_num__in=prof_qs.values('lic_num'))
    elif professional_type.upper() == DESIGNER:
        ret_qs = Designer.objects.filter(lic_num__in=prof_qs.values('lic_num'))
    else:
        raise UndefinedProfessionalType("Error: undefined professional type in search_by_zipcode")

    return ret_qs


class UndefinedProfessionalType(Exception):
    pass
