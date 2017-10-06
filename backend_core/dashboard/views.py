# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.utils import CONSUMER, PROFESSIONAL
# Create your views here.


@login_required
def show_dashboard(request, **kwargs):
    if request.user.role == CONSUMER:
        return render(request, 'dashboard/consumer_dashboard.html')
    else:
        return render(request, 'dashboard/professional_dashboard.html')


@login_required
def edit_success(request, **kwargs):
    return render(request, 'edit_success/edit_success.html')
