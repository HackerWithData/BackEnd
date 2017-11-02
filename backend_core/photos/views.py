# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from forms import PhotoForm, FileFieldForm, BackgroundPhotoForm
from models import Photo, FileField, BackgroundPhoto
from contractors.models import Contractor
from django.contrib.contenttypes.models import ContentType
import datetime
import pytz
import os
from django.http import HttpResponseNotFound
from django.shortcuts import render,redirect

# Create your views here.
class BasicUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos/upload_photo.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            f = form.save(commit=False)
            contractor = Contractor.objects.get(pk='1025362')
            f.content_type = ContentType.objects.get(model='contractor')
            f.object_id = contractor.LicNum
            # print('test2')
            f.save()
            data = {'is_valid': True, 'name': f.img.name, 'url': f.img.url}
        else:
            # print('test3')
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
            if 'contractor' in request.path:
                model_type = 'contractor'
            elif 'designer' in request.path:
                model_type = 'designer'
            elif 'architect' in request.path:
                model_type = 'architect'
            success_url = "/"+model_type+"/"+o_id
            form = BackgroundPhotoForm(request.POST, request.FILES)
            if form.is_valid():
                bp, nonexist = BackgroundPhoto.objects.get_or_create(content_type=ContentType.objects.get(model=model_type),
                                                                    object_id=o_id)

                if not nonexist:
                    old_pic_path = bp.img.file.name
                    os.remove(old_pic_path)

                bp.img = form.cleaned_data.get('img')
                bp.title = form.cleaned_data.get('img').name
                bp.uploaded_at = datetime.datetime.now(pytz.timezone('UTC'))
                bp.save()

                return redirect(success_url)
        else:
            form = BackgroundPhotoForm()
        return render(request, template_name, {'form': form})
    else:
        return HttpResponseNotFound('No Pages Found.')

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
