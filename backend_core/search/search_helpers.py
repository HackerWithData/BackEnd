import urllib

from django.forms.models import model_to_dict
from django.db.models import Q

from professionals.models import (CONTRACTOR, PROFESSIONAL_CHOICES,)

from professionals.utils import get_professional_instance, get_professionals
from hscore.utils import get_hscore, convert_hscore_to_rank
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
        name = str(search_target)
        lic = int(search_target)
        prof_qs_name = get_professionals(**{'name': name})
        prof_qs_lic = get_professionals(by_datacollection=True, **{'lic_num': lic})
        ret = [model_to_dict(prof) for prof in prof_qs_lic] + [model_to_dict(prof) for prof in prof_qs_name]
        return ret
    else:
        prof_qs = get_professionals(**{
            'name__icontains': search_target
        })
        ret = [model_to_dict(prof) for prof in prof_qs]
        return ret

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
            'pos_code': zipcode,
            'type': search_type,
            'professional_type__subtype': search_target,
        })
    else:
        prof_qs = get_professionals(**{
            'pos_code': zipcode
        })
    ret = [model_to_dict(prof) for prof in prof_qs]
    return ret


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
