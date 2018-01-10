import urllib

from django.forms.models import model_to_dict
from django.db.models import Q

from professionals.models import (
    CONTRACTOR,
    PROFESSIONAL_CHOICES,
)
from contractors.utils import convert_hscore_to_rank
from professionals.utils import get_professional_instance, get_professionals
from hscore.utils import get_hscore
# Ajax POST request
# def search_by_address_object(request):
#     zipcode = int(request['address']['address_components'][6]['short_name'])
#     target = request['target']
#     qs_prof = Professional.objects.filter(postal_code=zipcode)
#     # TODO: add subtype later
#     qs_prof_type = qs_prof.professionaltype_set.filter(type__icontains=target)
#     request['target'] =
#     return qs_prof_type

DEFAULT_NUM_PER_PAGE = 10


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
# search through zipcode
def search_by_name_or_lic(request):
    search_target = request.GET.get('target', '')
    # search target is whether a name or lic
    if search_target.isnumeric():
        name_or_lic = int(search_target)
        prof_qs = get_professionals(*(
            Q(name=str(name_or_lic)) | Q(lic_num=name_or_lic),
        ))
        # prof_qs = Professional.objects.filter(Q(name=str(name_or_lic)) | Q(lic_num=name_or_lic)).distinct()
    # elif search_target in [i[0] for i in PROFESSIONAL_CHOICES]:
    #     prof_qs = Professional.objects.filter(type=search_target)
    # # name search
    # elif search_target in [i[0] for i in PROFESSIONAL_SUBTYPE_CHOICES]:
    #     prof_qs = Professional.objects.filter(postal_code=zipcode, type=search_type,
    #                                           professional_type__subtype=search_target)
    else:
        prof_qs = get_professionals(**{
            'name__icontains': search_target
        })
        # prof_qs = Professional.objects.filter(name__icontains=search_target)
    # no result found
    if not prof_qs:
        return prof_qs.values()

    return retrieve_all_kind_professional(prof_qs)


# GET request
# search through zipcode
def search_by_zipcode(request):
    search_type = request.GET.get('type', '').upper()
    search_target = request.GET.get('target', '')
    zipcode = request.GET.get('zipcode', '')
    professionals = (pc[0] for pc in PROFESSIONAL_CHOICES)
    if search_type.upper() not in professionals:
        raise UndefinedProfessionalType("Error: undefined professional type in search_by_zipcode")

    # type search
    if search_target and search_type:
        prof_qs = get_professionals(**{
            'postal_code': zipcode,
            'type': search_type,
            'professional_type__subtype': search_target,
        })
    else:
        prof_qs = get_professionals(**{
            'postal_code': zipcode
        })
        # prof_qs = Professional.objects.filter(postal_code=zipcode).distinct()
    # retrieve corresponding professional through different table
    return retrieve_all_kind_professional(prof_qs)


def retrieve_all_kind_professional(prof_qs):
    ret_list = []
    for professional in prof_qs:
        model_type = professional.type.lower()
        instance = get_professional_instance(model_type=model_type, lic_num=professional.lic_num)
        item = model_to_dict(instance)
        item.update({'type': model_type.upper()})
        if model_type == 'contractor':
            hscore = get_hscore(contractor_id=instance.lic_num)
            if hscore is not None:
                item.update({
                    'score': hscore.score,
                    'rank': convert_hscore_to_rank(hscore),
                })
            else:
                item.update({
                    'score': None,
                    'rank': None,
                })
        ret_list.append(item)
    sorted_list = sorted(ret_list, key=lambda k: k.get('score', '') if k.get('type', None) == CONTRACTOR else 1000, reverse=True)
    return sorted_list


class UndefinedProfessionalType(Exception):
    pass
