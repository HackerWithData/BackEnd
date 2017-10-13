import urllib

from django.forms.models import model_to_dict

from contractors.models import Contractor
from designers.models import Designer
from architects.models import Architect
from professionals.models import Professional, ProfessionalType
from professionals.utils import ARCHITECT, DESIGNER, CONTRACTOR
from contractors.utils import convert_hscore_to_rank


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
    print search_type
    print search_target

    # mediate query set
    # name or lic num search
    if search_type.upper() == 'NAMEORLIC':
        # search target is whether a name or lic
        if search_target.isnumeric():
            name_or_lic = int(search_target)
            qs_prof_by_name = Professional.objects.filter(name=str(name_or_lic))
            qs_prof_by_lic = Professional.objects.filter(lic_num=name_or_lic)
            prof_qs = list(qs_prof_by_lic) + list(qs_prof_by_name)
        # name search
        else:
            prof_qs = Professional.objects.filter(name__icontains=search_target)
            # no result found
            if not prof_qs:
                return prof_qs.values()
            # retrieve type of value from name search
            # print prof_qs.values('type')[0]
            # professional = prof_qs.values('type')[0]['type'].upper()
    else:
        # type search
        prof_qs = Professional.objects.filter(postal_code=zipcode, type=search_type, professional_type__subtype=search_target)
        # professional = search_type.upper()

    # retrieve corresponding professional through different table
    ret_list = []
    for professional in prof_qs:
        if professional.type.upper() == CONTRACTOR:
            contractor = Contractor.objects.filter(lic_num=professional.lic_num).first()
            hscore = contractor.hscores.first()
            item = model_to_dict(contractor).copy()
            item['score'] = hscore.score
            item['rank'] = convert_hscore_to_rank(hscore)
            item['type'] = CONTRACTOR
            ret_list.append(item)
        elif professional.type.upper() == ARCHITECT:
            architect = Architect.objects.filter(lic_num=professional.lic_num).first()
            item = model_to_dict(architect).copy()
            item['type'] = ARCHITECT
        elif professional.type.upper() == DESIGNER:
            designer = Designer.objects.filter(lic_num=professional.lic_num).first()
            item = model_to_dict(designer).copy()
            item['type'] = DESIGNER
        else:
            raise UndefinedProfessionalType("Error: undefined professional type in search_by_zipcode")
        ret_list.append(item)

    return ret_list


class UndefinedProfessionalType(Exception):
    pass
