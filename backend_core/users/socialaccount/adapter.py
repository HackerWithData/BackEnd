from django.shortcuts import redirect

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.compat import is_authenticated


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    # def pre_social_login()
    def get_login_redirect_url(self, request):
        if 'project_success_url' in self.request.session:
            success_url = self.request.session['project_success_url']
        else:
            success_url = '/'
        print(success_url)
        return success_url

    def save_user(self, request, sociallogin, form=None):
        super(DefaultSocialAccountAdapter, self).save_user(request, sociallogin, form=form)
        if 'project_success_url' in self.request.session:
            success_url = self.request.session['project_success_url']
        else:
            success_url = '/'
        print(success_url)
        return redirect(success_url)

    def get_connect_redirect_url(self, request, socialaccount):
        assert is_authenticated(request.user)
        if 'project_success_url' in self.request.session:
            success_url = self.request.session['project_success_url']
        else:
            success_url = '/'
        print(success_url)
        return success_url
