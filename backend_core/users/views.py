# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.dispatch import receiver
from allauth.account.signals import user_logged_in

from utils import ROLE_CHOICES, PROFESSIONAL, CONSUMER
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from social_django.models import UserSocialAuth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from utils import *

@login_required
def sign_up_complete_info(request, **kwargs):
    if request.user.role == CONSUMER:
        return render(request, 'before_complete_consumer/before_complete_consumer.html')
    elif request.user.role == PROFESSIONAL:
        return render(request, 'before_complete_professional/before_complete_professional.html')
    else:
        raise UnexpectedMultipleChoice('Unexpected value for user role')

    # user = kwargs.pop('user')
    # user.role = user.role.lower().capitalize()
    #
    # if user.role == dict(ROLE_CHOICES).get(CONSUMER):
    #     # consumer
    #     print '1'
    #     return render(request, 'before_complete_consumer/before_complete_consumer.html')
    # elif user.role == dict(ROLE_CHOICES).get(PROFESSIONAL):
    #     # professional
    #     print '2'
    #     pass
    # else:
    #     print '3'
    #     raise UnexpectedMutipleChoice("Unexpected multiple choices for user type")



#qwer123456
# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(email=email, password=raw_password)
#             login(request, user)
#             return redirect('home_index')
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/signup.html', {'form': form})
#
#
# @login_required
# def settings(request):
#     user = request.user
#
#     try:
#         github_login = user.social_auth.get(provider='github')
#     except UserSocialAuth.DoesNotExist:
#         github_login = None
#     try:
#         twitter_login = user.social_auth.get(provider='twitter')
#     except UserSocialAuth.DoesNotExist:
#         twitter_login = None
#     try:
#         facebook_login = user.social_auth.get(provider='facebook')
#     except UserSocialAuth.DoesNotExist:
#         facebook_login = None
#
#     try:
#         google_login = user.social_auth.get(provider='google-oauth2')
#     except UserSocialAuth.DoesNotExist:
#         google_login = None
#
#     can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
#     return render(request, 'registration/settings.html', {
#         'github_login': github_login,
#         'twitter_login': twitter_login,
#         'facebook_login': facebook_login,
#         'google_login': google_login,
#         'can_disconnect': can_disconnect
#     })
#
# @login_required
# def password(request):
#     if request.user.has_usable_password():
#         PasswordForm = PasswordChangeForm
#     else:
#         PasswordForm = AdminPasswordChangeForm
#
#     if request.method == 'POST':
#         form = PasswordForm(request.user, request.POST)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordForm(request.user)
#     return render(request, 'users/password.html', {'form': form})