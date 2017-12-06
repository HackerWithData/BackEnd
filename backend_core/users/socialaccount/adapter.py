from django.conf import settings

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.compat import is_authenticated, reverse


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        """
        Returns the default URL to redirect to after successfully
        connecting a social account.
        """
        print('yes')
        assert is_authenticated(request.user)
        if 'success_url' in request.session:
            print(request.session['success_url'])
            success_url = request.session['success_url']
            del request.session['success_url']
        elif 'next' in request.path:
            success_url = request.GET['next']
        else:
            success_url = reverse('socialaccount_connections')
        return success_url
