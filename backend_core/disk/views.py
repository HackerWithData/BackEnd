# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import UserForm
from models import UserFile

# Create your views here.

def uploads(request):
    if request.method == 'POST':
        userform = UserForm(request.POST, request.FILES)
        if userform.is_valid():
            uf = UserFile()
            uf.userName = userform.cleaned_data['userName']
            uf.uploadFile = userform.cleaned_data['uploadFile']
            uf.save()
            return render(request,'disk/uploadsuccess.html')
    else:
        userform = UserForm(initial = {'userName': 'sunshore'})
    return render(request, 'disk/upload.html',{'userform':userform})

