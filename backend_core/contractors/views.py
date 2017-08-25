# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from contractors.models import Contractor

# Create your views here.

def display_contractor(request, slug):
    slug = '1025362'
    contractor = Contractor.objects.get(LicNum=slug)
    photo = 'asdasdqwacx'


    info_dict = {"contractor": contractor,'photo':photo}

    return render(request, 'contractor/contractor.html', {"info_dict" : info_dict})
