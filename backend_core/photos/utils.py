from .models import BackgroundPhoto, Photo
from .forms import PhotoForm
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _,  ugettext_lazy as _
from django.http import Http404
from review.utils import get_p_lic_num

def get_background_photo(model_name, object_id):
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


def display_project_photo(request, o_id, model):
    if request.is_ajax() and request.method == "POST":
        template_name = 'contractor/contractor_project_photo.html'
        model_name = str(ContentType.objects.get_for_model(model=model).name)
        instance = model.objects.get(lic_num=o_id)
        project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model=model_name),
                                              object_id=o_id)
        info_dict = {'project_photos': project_photos, model_name: instance}
        return render(request, template_name, {'info_dict': info_dict})
    else:
        raise Http404(_('No Pages Found.'))


def upload_project_photo(request, o_id, success_url, model_name):
    p_lic_num = get_p_lic_num(request)
    if str(p_lic_num) == str(o_id):
        template_name = 'contractor/contractor_project_photos_upload.html'  # Replace with your template.
        if request.method == "POST":
            form = PhotoForm(request.POST, request.FILES)
            content_type = ContentType.objects.get(model=model_name)
            object_id = int(o_id)
            files = request.FILES.getlist('img')
            if form.is_valid():
                if len(files) > 0:
                    for f in files:
                        instance = Photo.objects.create(img=f, title=f.name, content_type=content_type,
                                                        object_id=object_id)
                        instance.save()
                else:
                    pass
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
