from random import randint

from django.db.models.aggregates import Count
from django.core.exceptions import ObjectDoesNotExist
import random
import string
from users.models import User
from contractors.models import Contractor
from designers.models import Designer
from architects.models import Architect
from meisters.models import Meister
from professionals.models import Professional
from professionals.utils import CONTRACTOR, ARCHITECT, DESIGNER, MEISTER
from .models import HoomeId
from .utils import AVAILABLE


def get_professional_user(user):
    professional_profile = user.professional_profiles.first()
    professional = professional_profile.professional
    return professional


def get_user_by_hoome_id(hoome_id):
    user = User.objects.get(hoome_id=hoome_id)
    return user


def get_professional_corresponding_object_by_type_and_lic(prof_type, lic):
    if prof_type == CONTRACTOR:
        ret_professional_object = Contractor.objects.get(lic_num=lic)
    elif prof_type == ARCHITECT:
        ret_professional_object = Architect.objects.get(lic_num=lic)
    elif prof_type == DESIGNER:
        ret_professional_object = Designer.objects.get(lic_num=lic)
    elif prof_type == MEISTER:
        ret_professional_object = Meister.objects.get(lic_num=lic)
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
    elif prof_type == MEISTER:
        ret_professional_object = Meister.objects.get(lic_num=professional.lic_num)
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
        ret_professional_object = Contractor.objects.create(lic_num=lic, lic_status="Active")
    elif prof_type == ARCHITECT:
        ret_professional_object = Architect.objects.create(lic_num=lic, lic_status="Active")
    elif prof_type == DESIGNER:
        ret_professional_object = Designer.objects.create(lic_num=lic)
    elif prof_type == MEISTER:
        ret_professional_object = Meister.objects.get(lic_num=lic)
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


def generate_random_hoome_id():
    # randint(10000000,99999999)
    count = HoomeId.objects.filter(status=AVAILABLE).count()
    random_index = randint(0, count - 1)
    random_id = HoomeId.objects.filter(status=AVAILABLE)[random_index].hoome_id
    return random_id


def password_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))