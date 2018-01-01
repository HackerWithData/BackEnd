import re

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

from .utils import get_a_uuid, WAITING, PAID_TO_PROFESSIONAL, PAID_TO_HOOME

from .models import Project, ProjectPhoto, ProjectAttachment, Milestone
from users.utils import CONSUMER, PROFESSIONAL
from users.user_helpers import get_professional_user, get_user_by_hoome_id


def _save_milestone(amount, project):
    flag = True
    while flag:
        try:
            milestone_uuid = get_a_uuid()
            Milestone.objects.get(uuid=milestone_uuid)
        except Milestone.DoesNotExist:
            flag = False
    Milestone.objects.create(amount=amount, project=project,
                             uuid=milestone_uuid)


def save_milestone(request, project):
    list_amount = []
    for key,value in request.POST.items():
        reg = re.match("form-(\d)-amount", key)
        if reg:
            index = reg.group(1)
            try:
                if value == "" or value is None:
                    pass
                else:
                    list_amount.append([int(index), key])
            except:
                pass

    list_amount = sorted(list_amount, key=lambda x: x[0])
    for item in list_amount:
        _save_milestone(amount=request.POST[item[1]], project=project)


def save_project(request, project_form, professional_type=None, lic_id=None):
    project = project_form.save_project(commit=False)
    # pro means the professional in Professional model
    if professional_type and lic_id:
        content_type = ContentType.objects.get(model=professional_type.lower())
        professional = content_type.model_class().objects.get(lic_num=lic_id)
        lic_id = int(professional.lic_id)
        # save project
        project = project_form.save_project(commit=False)
        if request.user.is_authenticated:  # when user is logged in
            project.user = request.user
        project.content_type = content_type
        project.object_id = lic_id
        project.bus_name = professional.lic_name
    else:
        if project_form.cleaned_data['created_by'] == CONSUMER:
            pro = get_professional_user(get_user_by_hoome_id(project_form.cleaned_data['professional_hoome_id']))
            project.content_type = ContentType.objects.get(model=pro.type.lower())
            professional = project.content_type.model_class().objects.get(lic_num=pro.lic_num)
            project.object_id = int(professional.lic_id)
            project.bus_name = pro.name
            if request.user.is_authenticated:  # when user is logged in
                project.user = request.user
        elif project_form.cleaned_data['created_by'] == PROFESSIONAL:
            project.user = get_user_by_hoome_id(project_form.cleaned_data['homeowner_hoome_id'])
            if request.user.is_authenticated:  # when user is logged in
                pro = get_professional_user(request.user)
                project.content_type = ContentType.objects.get(model=pro.type.lower())
                professional = project.content_type.model_class().objects.get(lic_num=pro.lic_num)
                project.object_id = int(professional.lic_id)
                project.bus_name = pro.name

    project.save()
    return project


def save_project_attachment(request, project, project_form):
    files = request.FILES.getlist('project_attachment')
    if len(files) > 0:
        for f in files:
            ProjectAttachment.objects.create(project_attachment=f, title=f.name, project=project,
                                             attachment_type=project_form.cleaned_data['attachment_type'])
    else:
        pass


def save_project_photo(request, project):
    files = request.FILES.getlist('project_photo')
    if len(files) > 0:
        for f in files:
            ProjectPhoto.objects.create(project_photo=f, title=f.name, project=project)
    else:
        pass



def milestone_status_explanation(request, status):
    """
    explain each status of milestone
    :param request:
    :param status:
    :return: the explanation of each milestone status
    """
    explanation = None
    if status == WAITING:
        if request.user.role == CONSUMER:
            explanation = _("Waiting for homeowner make the payment.")
        elif request.user.role == PROFESSIONAL:
            explanation = _("Waiting for homeowner make the payment.")
    elif status == PAID_TO_HOOME:
        if request.user.role == CONSUMER:
            explanation = _("Hoome has recevied the payment and will hold for you.")
        elif request.user.role == PROFESSIONAL:
            explanation = _("Hoome has recevied the payment and please start to work.")
    elif status == PAID_TO_PROFESSIONAL:
        if request.user.role == CONSUMER:
            explanation = _("You have allowed Hoome release the payment.")
        elif request.user.role == PROFESSIONAL:
            explanation = _("Homeowner have released the payment for current milestone.")
    return explanation
