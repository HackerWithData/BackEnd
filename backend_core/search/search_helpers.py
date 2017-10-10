import urllib

from contractors.models import Contractor
from designers.models import Designer
from architects.models import Architect
from professionals.models import Professional, ProfessionalType
from professionals.utils import ARCHITECT, DESIGNER, CONTRACTOR


# Ajax POST request
# def search_by_address_object(request):
#     zipcode = int(request['address']['address_components'][6]['short_name'])
#     target = request['target']
#     qs_prof = Professional.objects.filter(postal_code=zipcode)
#     # TODO: add subtype later
#     qs_prof_type = qs_prof.professionaltype_set.filter(type__icontains=target)
#     request['target'] =
#     return qs_prof_type


# Ajax POST request
def search_by_address_object_redirect_url(request):
    print request
    zipcode = int(request['address']['address_components'][6]['short_name'])
    search_type = request['type']
    search_target = request['target']
    url_parameters = {
        'zipcode': zipcode,
        'target': search_target,
        'type': search_type,
    }
    return urllib.urlencode(url_parameters)


# GET request
# search through zipcode
def search_by_zipcode(request):
    search_type = request.GET['type'].upper()
    search_target = request.GET['target']
    zipcode = request.GET['zipcode']

    # mediate query set
    if search_type.upper() == 'NAME':
        # name search
        qs_prof = Professional.objects.filter(name__iexact=search_target)
        prof_qs = qs_prof
        if not prof_qs:
            return prof_qs
        # retrieve type of value from name search
        professional = prof_qs.values('type')[0].upper()
    else:
        # type search
        prof_qs = Professional.objects.filter(postal_code=zipcode, type=search_type, professional_type__subtype=search_target)
        professional = search_type.upper()

    # retrieve corresponding professional through different table
    if professional == CONTRACTOR:
        ret_qs = Contractor.objects.filter(lic_num__in=prof_qs.values('lic_num')).order_by('-hscore__score')
    elif professional == ARCHITECT:
        ret_qs = Architect.objects.filter(lic_num__in=prof_qs.values('lic_num'))
    elif professional == DESIGNER:
        ret_qs = Designer.objects.filter(lic_num__in=prof_qs.values('lic_num'))
    else:
        raise UndefinedProfessionalType("Error: undefined professional type in search_by_zipcode")

    return ret_qs, professional


class UndefinedProfessionalType(Exception):
    pass
