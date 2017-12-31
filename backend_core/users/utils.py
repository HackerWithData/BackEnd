import json
import os

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

# role type
PROFESSIONAL = 'PROFESSIONAL'
CONSUMER = 'CONSUMER'
ROLE_CHOICES = (
    (PROFESSIONAL, _('Professional')),
    (CONSUMER, _('Consumer')),
)

# gender type
MALE = 'MALE'
FEMALE = 'FEMALE'
GENDER_CHOICES = (
    (MALE, _('Male')),
    (FEMALE, _('Female')),
)

HOLD = "H"
SIGNED = "S"
AVAILABLE = "A"
BAD = 'B'
ID_STATUS = (
    (HOLD, _("Hold")),
    (BAD, _("Bad")),
    (SIGNED, _("Signed")),
    (AVAILABLE, _("Available")),
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


class SocialAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        check for data and save what you want.

        :param request:
        :param sociallogin:
        :return:
        """
        user = sociallogin.account.user
        user.first = sociallogin.account.data['first_name']

    def populate_user(self, request, sociallogin, data):
        """
        save data during social signup

        :param request:
        :param sociallogin:
        :param data:
        :return:
        """
        user = sociallogin.account.user
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.username = data['username']
        user.email = data['email']


class UnexpectedMultipleChoice(Exception):
    pass
