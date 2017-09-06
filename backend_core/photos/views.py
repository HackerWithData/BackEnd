# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from forms import PhotoForm,FileFieldForm
from models import Photo, FileField
#from django.views.generic.edit import FormView

from django.contrib.contenttypes.models import ContentType

class BasicUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos/upload_photo.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        print('test1')
        print(vars(form))
        print(form.errors)
        form.content_type = request.POST['content_type']
        form.object_id = request.POST['object_id']
        if form.is_valid():
            print('test2')
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            print('test3')
            data = {'is_valid': False}
        return JsonResponse(data)


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