from django.shortcuts import redirect

# from allauth.socialaccount.adapter import DefaultSocialAccountAdapter as
from allauth.account.adapter import DefaultAccountAdapter
# from .user_helpers import generate_random_hoome_id
from allauth.account.utils import get_next_redirect_url
from allauth.account.adapter import get_adapter


class MyAccountAdapter(DefaultAccountAdapter):
    # def save_user(self, request, user, form, commit=True):
    #     from allauth.account.utils import user_username, user_email, user_field
    #
    #     data = form.cleaned_data
    #     first_name = data.get('first_name')
    #     last_name = data.get('last_name')
    #     email = data.get('email')
    #     username = data.get('username')
    #     user_email(user, email)
    #     user_username(user, username)
    #     if first_name:
    #         user_field(user, 'first_name', first_name)
    #     if last_name:
    #         user_field(user, 'last_name', last_name)
    #     if 'password1' in data:
    #         user.set_password(data["password1"])
    #     else:
    #         user.set_unusable_password()
    #     self.populate_username(request, user)
    #     user.hoome_id = generate_random_hoome_id()
    #     if commit:
    #         # Ability not to commit makes it easier to derive from
    #         # this adapter by adding
    #         user.save()
    #     return user


    def get_login_redirect_url(self, request, url=None, redirect_field_name="next"):
        if 'project_success_url' in request.session:
            redirect_url = request.session['project_success_url']
            del request.session['project_success_url']
        elif 'success_url' in request.session:
            redirect_url = request.session['success_url']
            del request.session['success_url']
        else:
            # redirect_url = '/'
            if url and callable(url):
                # In order to be able to pass url getters around that depend
                # on e.g. the authenticated state.
                url = url()
            redirect_url = (get_next_redirect_url(
                request,
                redirect_field_name=redirect_field_name) or
                            url)
        return redirect_url
