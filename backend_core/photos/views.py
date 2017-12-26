# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import pytz
import os

from django.http import JsonResponse
from django.views import View
from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.conf import settings

import boto
from boto.s3.key import Key

from professionals.utils import check_professional_type
from forms import PhotoForm, FileFieldForm, BackgroundPhotoForm
from models import Photo, FileField, BackgroundPhoto
from contractors.models import Contractor
from .utils import (
    get_photo_list,
    upload_bg_photo,
)
from .forms import (
    get_photo_form,
    get_bgphoto_form,
)

# Create your views here.


class BasicUploadView(View):
    def get(self, request):
        photos_list = get_photo_list()
        return render(request, 'photos/upload_photo.html', {'photos': photos_list})

    def post(self, request):
        form = get_photo_form(request=request, method='POST')
        if form.is_valid():
            f = form.save(commit=False)
            contractor = Contractor.objects.get(pk='1025362')
            f.content_type = ContentType.objects.get(model='contractor')
            f.object_id = contractor.LicNum
            f.save()
            data = {'is_valid': True, 'name': f.img.name, 'url': f.img.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


# @login_required
def background_photo_upload(request, o_id):
    if request.user.is_anonymous():
        p_lic_num = None
    else:
        try:
            p_lic_num = int(request.user.professional_profiles.first().professional.lic_num)
        except:
            p_lic_num = None

    if str(p_lic_num) == str(o_id):
        template_name = 'photos/background_photo_upload.html'
        if request.method == 'POST':
            model_type = check_professional_type(request)
            success_url = "/" + model_type + "/" + o_id
            form = get_bgphoto_form(request=request, method="POST")
            if form.is_valid():
                upload_bg_photo(
                    request=request,
                    form=form,
                    model_name=model_type,
                    o_id=o_id
                )
                return redirect(success_url)
        else:
            form = get_bgphoto_form(request=request, method='GET')
        return render(request, template_name, {'form': form})
    else:
        raise Http404('No Pages Found.')

#this funtion is deprecated
def FileFieldUpload(request):
    template_name = 'photos/upload_multiple_files.html'  # Replace with your template.
    success_url = 'disk/uploadsuccess.html'  # Replace with your URL or reverse().

    if request.method == "POST":
        form = FileFieldForm(request.POST, request.FILES)
        files = request.FILES.getlist('img')
        if form.is_valid():
            for f in files:
                instance = FileField.objects.create(img=f, title=f.name, object_id=18,
                                                    content_type=ContentType.objects.get_for_model(
                                                        settings.AUTH_USER_MODEL))
                instance.save()
            return render(request, success_url)
    form = FileFieldForm()

    return render(request, template_name, {"form": form})
