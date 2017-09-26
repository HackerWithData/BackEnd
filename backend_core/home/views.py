# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import os


# Create your views here.
def index(request):
    bg_img_path = os.listdir(r'media/background-pic/')
    info_dict = {"background": bg_img_path}
    # print bg_img_path
    return render(request, 'home/home.html', info_dict)
