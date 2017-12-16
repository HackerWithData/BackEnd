import json

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _, ugettext_lazy as _
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse

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


def get_project_photos(model_name, object_id):
    project_photos = Photo.objects.filter(
        content_type=ContentType.objects.get(model=model_name),
        object_id=object_id
    )
    return project_photos


def display_project_photo(request, o_id, model, template_name):
    if request.is_ajax() and request.method == "POST":
        model_name = str(ContentType.objects.get_for_model(model=model).name)
        instance = model.objects.get(lic_num=o_id)
        project_photos = get_project_photos(model_name=model_name, object_id=o_id)
        info_dict = {'project_photos': project_photos, model_name: instance}
        return render(request, template_name, {'info_dict': info_dict})
    else:
        raise Http404(_('No Pages Found.'))


def upload_photo(request, o_id, model_name):
    content_type = ContentType.objects.get(model=model_name)
    object_id = int(o_id)
    files = request.FILES.getlist('img')
    if len(files) > 0:
        for f in files:
            instance = Photo.objects.create(img=f, title=f.name, content_type=content_type,
                                            object_id=object_id)
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


def delete_photo(request, contractor_id):
    if request.is_ajax() and request.method == "POST":
        if contractor_id:
            contractor_id = int(contractor_id)
        p_lic_num = get_p_lic_num(request)
        if p_lic_num == contractor_id:
            data = {}
            data.update(json.loads(request.body))
            # print(data)
            photo_id = data.get('id', None)
            if photo_id is not None:
                photo = Photo.objects.get(id=photo_id)
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
