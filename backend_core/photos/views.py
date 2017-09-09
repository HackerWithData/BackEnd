# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from forms import PhotoForm, FileFieldForm, BackgroundPhotoForm
from models import Photo, FileField, BackgroundPhoto
#from django.views.generic.edit import FormView
from contractors.models import Contractor
from django.contrib.contenttypes.models import ContentType
import datetime


# Create your views here.
class BasicUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos/upload_photo.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        #print('test1')
        #print(vars(form))
        #print(form.errors)

        if form.is_valid():
            f = form.save(commit=False)
            contractor = Contractor.objects.get(pk='1025362')
            f.content_type = ContentType.objects.get(model='contractor')
            f.object_id = contractor.LicNum
            #print('test2')
            f.save()
            data = {'is_valid': True, 'name': f.img.name, 'url': f.img.url}
        else:
            #print('test3')
            data = {'is_valid': False}
        return JsonResponse(data)

#@login_required
def background_photo_upload(request):
    template_name = 'photos/background_photo_upload.html'
    success_url = "disk/uploadsuccess.html"
    if request.method == 'POST':
        form = BackgroundPhotoForm(request.POST, request.FILES)

        if form.is_valid():
            contractor = Contractor.objects.get(pk='1025362')
            BP = BackgroundPhoto.objects.get_or_create(content_type=ContentType.objects.get(model='contractor'),
                                                       object_id=contractor.LicNum)[0]
            print(BP)
            BP.img = form.cleaned_data.get('img')
            BP.uploaded_at = datetime.datetime.now()


            BP.save()
            return render(request, success_url)
    else:
        form = BackgroundPhotoForm()
    return render(request, template_name, {'form': form})

def FileFieldUpload(request):
    template_name = 'photos/upload_multiple_files.html'  # Replace with your template.
    success_url = 'disk/uploadsuccess.html'  # Replace with your URL or reverse().

    if request.method == "POST":
        form = FileFieldForm(request.POST, request.FILES)
        files = request.FILES.getlist('img')
        if form.is_valid():
            for f in files:
                instance = FileField.objects.create(img=f, title=f.name, object_id=18, content_type=ContentType.objects.get(model='user'))
                instance.save()
            return render(request, success_url)
    form = FileFieldForm()

    return render(request, template_name, {"form": form})

#
# def FileFieldUpload(request):
#     #form_class = FileFieldForm
#     template_name = 'photos/upload_multiple_files.html'  # Replace with your template.
#     success_url = 'disk/uploadsuccess.html'  # Replace with your URL or reverse().
#
#     if request.method == "POST":
#         #form_class = self.get_form_class()
#         #form = self.get_form(form_class)
#         files = request.FILES.getlist('myfiles')
#         #if form.is_valid():
#         print(files)
#         for f in files:
#             print(f)
#             instance = FileField.objects.create(img = f, title=f.name)
#             instance.save()
#         return render(request, success_url)
#         #else:
#         #    return self.form_invalid(form)
#     return render(request, template_name)