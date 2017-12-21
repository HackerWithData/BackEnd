import json
import os

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _, ugettext_lazy as _
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings

import boto
from boto.s3.key import Key

from .models import BackgroundPhoto, Photo
from .forms import PhotoForm
from users.utils import get_p_lic_num


def get_bgimage(model_name, object_id):
    try:
        bgimage = BackgroundPhoto.objects.get(
            content_type=ContentType.objects.get(model=model_name),
            object_id=object_id
        )
    except:
        bgimage = None
    return bgimage


def get_photos(model_name, object_id):
    photos = Photo.objects.filter(
        content_type=ContentType.objects.get(model=model_name),
        object_id=object_id
    )
    return photos


def display_project_photo(request, o_id, model, template_name):
    if request.is_ajax() and request.method == "POST":
        model_name = str(ContentType.objects.get_for_model(model=model).name)
        instance = model.objects.get(lic_num=o_id)
        project_photos = get_photos(model_name=model_name, object_id=o_id)
        info_dict = {'project_photos': project_photos, model_name: instance}
        return render(request, template_name, {'info_dict': info_dict})
    else:
        raise Http404(_('No Pages Found.'))


def upload_photo(request, o_id, model_name):
    content_type = ContentType.objects.get(model=model_name)
    object_id = int(o_id)
    files = request.FILES.getlist('img')
    for f in files:
        instance = Photo.objects.create(
            img=f,
            title=f.name,
            content_type=content_type,
            object_id=object_id
        )
        instance.save()


def upload_project_photo(request, o_id, success_url, model_name, template_name):
    p_lic_num = get_p_lic_num(request)
    if str(p_lic_num) == str(o_id):
        if request.method == "POST":
            form = PhotoForm(request.POST, request.FILES)
            if form.is_valid():
                upload_photo(request=request, o_id=o_id, model_name=model_name)
                return redirect(success_url)
        form = PhotoForm()
        info_dict = {'form': form}
        return render(request, template_name, info_dict)
    else:
        raise Http404(_('No Pages Found.'))


def upload_bg_photo(request, form, model_name, o_id):
    bp, nonexist = BackgroundPhoto.objects.get_or_create(
        content_type=ContentType.objects.get(model=model_name),
        object_id=o_id
    )
    bp.img = form.cleaned_data.get('img')
    bp.title = form.cleaned_data.get('img').name
    bp.uploaded_at = datetime.datetime.now(pytz.timezone('UTC'))
    bp.save()
    if not nonexist:
        old_pic_path = bp.img.file.name
        if hasattr(settings, 'AWS_ACCESS_KEY_ID'):
            s3conn = boto.connect_s3(
                settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY
            )
            bucket = s3conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
            k = Key(bucket)
            k.key = str(old_pic_path)
            k.delete()
        else:
            os.remove(old_pic_path)


def delete_photo(request, contractor_id):
    if request.is_ajax() and request.method == "POST":
        if contractor_id:
            contractor_id = int(contractor_id)
        p_lic_num = get_p_lic_num(request)
        if p_lic_num == contractor_id:
            data = {}
            data.update(json.loads(request.body))
            photo_id = data.get('id', None)
            if photo_id is not None:
                photo = Photo.objects.get(id=photo_id)
                old_pic_path = photo.img.file.name
                if hasattr(settings, 'AWS_ACCESS_KEY_ID'):
                    s3conn = boto.connect_s3(
                        settings.AWS_ACCESS_KEY_ID,
                        settings.AWS_SECRET_ACCESS_KEY
                    )
                    bucket = s3conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
                    k = Key(bucket)
                    k.key = str(old_pic_path)
                    k.delete()
                else:
                    os.remove(old_pic_path)
                photo.delete()
                response_data = {'success': 'photo is deleted successfully'}
                return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)
            else:
                response_data = {'error': 'photo_id is empty'}
                return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)
        else:
            response_data = {'error', 'deletion request is not from its owner'}
            return HttpResponse(response_data, content_type='application/json', status=200)
    else:
        raise Http404


def get_photo_list():
    return Photo.objects.all()

