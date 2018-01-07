# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from allauth.account.decorators import verified_email_required
from users.utils import CONSUMER, PROFESSIONAL
# Create your views here.


@login_required
@verified_email_required
def show_dashboard(request, **kwargs):
    return render(request, 'dashboard/dashboard.html')


@login_required
@verified_email_required
def edit_success(request, **kwargs):
    return render(request, 'edit_success/edit_success.html')
