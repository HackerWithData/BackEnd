# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render
import os
from datetime import datetime

# Create your views here.
def index(request):
    # it is ok to use absolute path here bacause it is used to get list of image name rather than serve them
    counter = str(datetime.today().day)[-1]
    background = [file for file in os.listdir(os.path.join(settings.BASE_DIR, 'static', 'image', 'background-pic','bg_set')) if ('slider_' + str(counter)) in file]
    return render(request, 'home/home.html', {'background': background})
