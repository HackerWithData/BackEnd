# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render
import os
from datetime import datetime
from django.shortcuts import render_to_response
from django.http import Http404

# Create your views here.
def index(request):
    # it is ok to use absolute path here bacause it is used to get list of image name rather than serve them
    counter = str(datetime.today().day)[-1]
    background = [file for file in os.listdir(os.path.join(settings.BASE_DIR, 'static', 'image', 'background-pic','bg_set')) if ('slider_' + str(counter)) in file]
    # raise Http404()
    return render(request, 'home/home.html', {'background': background})


def page_not_found(request):
    return render(request, '404.html')


def server_error(request):
    return render(request, '500.html')


def permission_denied(request):
    return render(request, '403.html')


def bad_request(request):
    return render(request, '400.html')