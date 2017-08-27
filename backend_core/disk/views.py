# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import UserForm,ImageForm
from models import UserFile,ProjectImage
from django.forms import modelformset_factory
# Create your views here.

def uploads(request):
    print(request.path)
    if 'projectphoto' not in request.path:
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

    elif 'projectphoto' in request.path:
        ImageFormSet = modelformset_factory(ProjectImage, fields = ('userName','image', ),
                                            form=ImageForm, extra=3)
        #print(vars(ImageFormSet))
        #print('\n\n\n\n\n')
        if request.method == 'POST':

            formset = ImageFormSet(request.POST, request.FILES,
                                   queryset=ProjectImage.objects.none())

            if formset.is_valid():
                for form in formset.cleaned_data:
                    photo = ProjectImage()
                    photo.userName = form['userName']
                    photo.image = form['image']
                    photo.save()
                return render(request,'disk/uploadsuccess.html')
        else:
            formset = ImageFormSet(queryset=ProjectImage.objects.none())
        return render(request, 'disk/projectphoto.html',{'formset': formset})

