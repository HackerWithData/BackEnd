# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'test': 'just for test.',
        'welcome': 'hello world.'
    }
    return render(request, 'home_index.html', context)