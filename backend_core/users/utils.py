from django.conf import settings

import json
import os

# role type
PROFESSIONAL = 'PROFESSIONAL'
CONSUMER = 'CONSUMER'
ROLE_CHOICES = (
    (PROFESSIONAL, 'Professional'),
    (CONSUMER, 'Consumer'),
)

# gender type
MALE = 'MALE'
FEMALE = 'FEMALE'
GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
)

# TODO: load static file into professional subtype
def setup_professional_type():
    dir_path = os.path.join(settings.BASE_DIR, 'static', 'json', 'subtype.json')
    try:
        json_professional_file = open(dir_path)
        json_str = json_professional_file.read()
        professional = json.loads(json_str)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    finally:
        json_professional_file.close()

    return professional


class UnexpectedMultipleChoice(Exception):
    pass
