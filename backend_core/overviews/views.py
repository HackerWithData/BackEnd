# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from forms import OverviewForm
from models import Overview
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
# Create your views here.
from professionals.utils import check_professional_type

def edit_overview(request, o_id):
    overview_form = OverviewForm(request.POST)
    # TODO: assign a random password
    if overview_form.is_valid():
        # User = #ContentType.objects.get_for_model(settings.AUTH_USER_MODEL)
        model_type = check_professional_type(request)
        overview, status = Overview.objects.get_or_create(content_type=ContentType.objects.get(model=model_type), object_id=o_id)
        overview.overview = overview_form.cleaned_data['overview']
        overview.save()
        messages.success(request, _('Request Success'))
    else:
        messages.warning(request, _('Request Failed'))