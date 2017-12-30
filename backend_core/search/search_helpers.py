import urllib

from django.forms.models import model_to_dict
from django.db.models import Q

from contractors.models import Contractor
from designers.models import Designer
from architects.models import Architect
from meisters.models import Meister
from professionals.models import Professional, ProfessionalType
from professionals.utils import ARCHITECT, DESIGNER, CONTRACTOR, PROFESSIONAL_CHOICES, PROFESSIONAL_SUBTYPE_CHOICES, \
    MEISTER
from contractors.utils import convert_hscore_to_rank
from hscore.models import Hscore

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
def search_by_name_or_lic(request):
    search_target = request.GET['target']
    # search target is whether a name or lic
    if search_target.isnumeric():
        name_or_lic = int(search_target)
        prof_qs = Professional.objects.filter(Q(name=str(name_or_lic)) | Q(lic_num=name_or_lic)).distinct()
    # elif search_target in [i[0] for i in PROFESSIONAL_CHOICES]:
    #     prof_qs = Professional.objects.filter(type=search_target)
    # # name search
    # elif search_target in [i[0] for i in PROFESSIONAL_SUBTYPE_CHOICES]:
    #     prof_qs = Professional.objects.filter(postal_code=zipcode, type=search_type,
    #                                           professional_type__subtype=search_target)
    else:
        prof_qs = Professional.objects.filter(name__icontains=search_target)
    # no result found
    if not prof_qs:
        return prof_qs.values()

    return retrieve_all_kind_professional(prof_qs)


# GET request
# search through zipcode
def search_by_zipcode(request):
    search_type = request.GET['type'].upper()
    search_target = request.GET['target']
    zipcode = request.GET['zipcode']
    # type search
    if search_target and search_type:
        prof_qs = Professional.objects.filter(postal_code=zipcode, type=search_type,
                                          professional_type__subtype=search_target).distinct()
    else:
        prof_qs = Professional.objects.filter(postal_code=zipcode).distinct()
    # retrieve corresponding professional through different table
    return retrieve_all_kind_professional(prof_qs)


def retrieve_all_kind_professional(prof_qs):
    ret_list = []
    for professional in prof_qs:
        if professional.type.upper() == CONTRACTOR:
            contractor = Contractor.objects.filter(lic_num=professional.lic_num).first()
            # print(contractor)
            # print(contractor.hscore)

            hscore = contractor.hscores.first()
            if hscore is None:
                hscore = Hscore.objects.create(contractor=contractor, score=None, rank=None, max=None)
            # print(contractor.lic_name, hscore.score)
            item = model_to_dict(contractor).copy()
            item['score'] = hscore.score
            item['rank'] = convert_hscore_to_rank(hscore)
            item['type'] = CONTRACTOR
        elif professional.type.upper() == ARCHITECT:
            architect = Architect.objects.filter(lic_num=professional.lic_num).first()
            item = model_to_dict(architect).copy()
            item['type'] = ARCHITECT
        elif professional.type.upper() == DESIGNER:
            designer = Designer.objects.filter(lic_num=professional.lic_num).first()
            item = model_to_dict(designer).copy()
            item['type'] = DESIGNER
        # TODO: need to take care this part.
        elif professional.type.upper() == MEISTER:
            meister = Meister.objects.filter(lic_num=professional.lic_num).first()
            item = model_to_dict(meister).copy()
            item['type'] = MEISTER
        else:
            raise UndefinedProfessionalType("Error: undefined professional type in search_by_zipcode")
        ret_list.append(item)

    sorted_list = sorted(ret_list, key=lambda k: k['score'] if k['type'] == CONTRACTOR else 1000, reverse=True)
    return sorted_list


class UndefinedProfessionalType(Exception):
    pass
