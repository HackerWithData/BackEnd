import warnings

from django.conf import settings
from django.shortcuts import resolve_url

from allauth.account.adapter import DefaultAccountAdapter
from allauth.compat import is_authenticated, reverse

from .utils import CONSUMER, PROFESSIONAL


class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        assert is_authenticated(request.user)
        # print('yes',1)
        if request.user.role == PROFESSIONAL and request.user.professional_profiles.first() is None:
            success_url = 'account_professional_profile_after_signup'
        else:
            if 'success_url' in request.session:
                success_url = request.session['success_url']
            elif 'next' in request.path:
                success_url = request.GET['next']
            else:
                success_url = getattr(settings, "LOGIN_REDIRECT_URLNAME", None)
                if success_url:
                    warnings.warn("LOGIN_REDIRECT_URLNAME is deprecated, simply"
                                  " use LOGIN_REDIRECT_URL with a URL name",
                                  DeprecationWarning)
                else:
                    success_url = settings.LOGIN_REDIRECT_URL
        return resolve_url(success_url)
