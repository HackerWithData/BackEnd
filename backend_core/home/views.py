# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render
import os


# Create your views here.
def index(request):
    # it is ok to use absolute path here bacause it is used to get list of image name rather than serve them
    bg_img_path = os.listdir(os.path.join(settings.BASE_DIR, 'static', 'image', 'background-pic'))
    info_dict = {"background": bg_img_path}
    # print bg_img_path
    return render(request, 'home/home.html', info_dict)
