# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from professionals.utils import check_professional_type
from .forms import OverviewForm
from .models import Overview
from .utils import get_or_create_overview


def edit_overview(request, o_id):
    overview_form = OverviewForm(request.POST)
    # TODO: assign a random password
    if overview_form.is_valid():
        model_name = check_professional_type(request)
        content = overview_form.cleaned_data['overview']
        get_or_create_overview(
            content=content,
            model_name=model_name,
            o_id=o_id
        )
        messages.success(request, _('Request Success'))
    else:
        messages.warning(request, _('Request Failed'))