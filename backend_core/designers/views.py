# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Designer
from professionals.views import ProfessionalDetail


# TODO: add a overview database
class DesignerDetail(ProfessionalDetail):
    def __init__(self):
        super(DesignerDetail, self).__init__()
        self.template_name = 'designer/designer.html'
        self.data_source = 'NCIQ'
        self.model = Designer


def display_project_photos(request, o_id):
    if request.is_ajax() and request.method == "POST":
        template_name = 'designer/designer_project_photo.html'
        designer = Designer.objects.get(lic_num=o_id)
        project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='designer'),
                                              object_id=o_id)
        info_dict = {'project_photos': project_photos, 'designer': designer}
        return render(request, template_name, {'info_dict': info_dict})
    else:
        raise Http404('No Pages Found.')


# %% TODO: change function to accept all instance like architects or designers
def upload_project_photos(request, o_id):
    if request.user.is_anonymous():
        p_lic_num = None
    else:
        try:
            p_lic_num = int(request.user.professional_profiles.first().professional.lic_num)
        except:
            p_lic_num = None

    if str(p_lic_num) == str(o_id):
        template_name = 'designer/designer_project_photos_upload.html'  # Replace with your template.
        success_url = '/designer/' + o_id  # Replace with your URL or reverse().

        if request.method == "POST":
            form = PhotoForm(request.POST, request.FILES)
            content_type = ContentType.objects.get(model='designer')
            files = request.FILES.getlist('img')
            if form.is_valid():
                if len(files) > 0:
                    for f in files:
                        instance = Photo.objects.create(img=f, title=f.name, content_type=content_type,
                                                        object_id=int(o_id))
                        instance.save()
                else:
                    pass
                return redirect(success_url)
        form = PhotoForm()
        info_dict = {'form': form}
        return render(request, template_name, info_dict)
    else:
        raise Http404('No Pages Found.')
