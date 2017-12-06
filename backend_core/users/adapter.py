import warnings

from django.conf import settings
from django.shortcuts import resolve_url

from allauth.account.adapter import DefaultAccountAdapter
from allauth.compat import is_authenticated, reverse


class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        assert is_authenticated(request.user)
        print('yes',1)
        if 'success_url' in request.session:
            print(request.session['success_url'])
            success_url = request.session['success_url']
            #del request.session['success_url']
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
