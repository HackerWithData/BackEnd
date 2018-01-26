from random import randint
import random
import string

from users.models import User, AVAILABLE, HoomeId, SIGNED
#from contractors.models import Contractor
#from designers.models import Designer
#from architects.models import Architect
from meisters.models import Meister
from professionals.models import (
    Professional,
    CONTRACTOR,
    ARCHITECT,
    DESIGNER,
    MEISTER,
)


def get_professional_user(user):
    professional_profile = user.professional_profiles.first()
    professional = professional_profile.professional
    return professional


def get_user_by_hoome_id(hoome_id):
    try:
        user = User.objects.get(hoome_id=hoome_id)
        return user
    except User.DoesNotExist:
        return None

#TODO: need to change the logic here. Here we want to search the data collection table by lic_num
def get_professional_corresponding_object_by_type_and_lic(prof_type, lic):
    try:
        ret_professional_object = Professional.objects.get(lic_num=lic)
    except:
        raise UndefinedType("Error: Undefined Type in Object")
    return ret_professional_object

#TODO: need to change the logic here. Here we want to search the data collection table by lic_num
def get_professional_corresponding_object_by_user(user):
    professional_profile = user.professional_profiles.first()
    professional = professional_profile.professional
    # prof_type = professional.type
    try:
        ret_professional_object = professional
    except:
        raise UndefinedType("Error: Undefined Type in Object")
    return ret_professional_object

#TODO: need to change the logic here. Here we want to search the data collection table by lic_num
def get_professional_and_professional_corresponding_object_by_user(user):
    professional_profile = user.professional_profiles.first()
    professional = professional_profile.professional
    ret_professional = professional
    prof_type = professional.type
    try:
        ret_professional_object = professional
    except:
     raise UndefinedType("Error: Undefined Type in Object")
    return ret_professional, ret_professional_object

#TODO: need to change the logic here. Here we want to search the data collection table by lic_num
def create_professional_corresponding_object(prof_type, lic):
    try:
        ret_professional_object = Professional.objects.get(lic_num=lic)
    except:
        raise UndefinedType("Error: Undefined Type in Object")
    return ret_professional_object

def retrieve_professional_info(request):
    prof_type = request.GET['type'].upper()
    lic = request.GET['lic']
    try:
        professional = Professional.objects.get(lic_num=lic, type=prof_type)
        professional_types = professional.professional_types.all()
        subtypes = [professional_type.subtype for professional_type in professional_types]
    except Professional.DoesNotExist:
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
    random_id = HoomeId.objects.filter(status=AVAILABLE)[random_index]
    random_id.status = SIGNED
    random_id.save()
    return random_id.hoome_id


def password_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
