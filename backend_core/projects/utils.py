import uuid

from django.contrib.contenttypes.models import ContentType

from .models import (
    ProjectAttachment,
    Project,
    Milestone,
    ProjectPhoto,
)
from users.models import CONSUMER, PROFESSIONAL


# get a UUID
def get_a_uuid(*argv):
    if len(argv) == 0:
        r_uuid = str(uuid.uuid4())
        return r_uuid
    elif len(argv) == 1:
        # in python 2.x TODO: need to add case in python 3.x
        if isinstance(argv[0], basestring):
            try:
                model = ContentType.objects.get(model=argv[0])
            except ContentType.DoesNotExist:
                print("Does Not Exist!")
        else:
            try:
                model = ContentType.objects.get_for_model(argv[0])
            except ContentType.DoesNotExist:
                print("Does Not Exist!")
        flag = True
        while flag:
            try:
                r_uuid = str(uuid.uuid4())
                object = model.get_object_for_this_type(uuid=r_uuid)
            except model.model_class().DoesNotExist:
                flag = False
        return r_uuid
    else:
        raise Exception('%d arguments given, which requires 1.' % (len(argv)))


def upload_project_attachment(request, project, form):
    files = request.FILES.getlist('project_attachment')
    if form.is_valid():
        for file in files:
            ProjectAttachment.objects.create(
                project_attachment=file,
                title=file.name,
                project=project,
                attachment_type=form.cleaned_data['attachment_type'],
            )
        return 'upload_success'
    return 'form_error'


def get_user_projects(user):
    if user.role == CONSUMER:
        projects = Project.objects.filter(user=user).order_by('-project_id')
        info_dict = {'projects': projects}
        return info_dict
    elif user.role == PROFESSIONAL:
        professional = user.professional_profiles.first().professional
        projects = Project.objects.filter(
            content_type=ContentType.objects.get(model=professional.type.lower()),
            object_id=int(professional.lic_num)
        ).order_by('-project_id')
        info_dict = {'projects': projects, 'professional': professional}
        return info_dict


def get_project(uuid_):
    try:
        project = Project.objects.get(uuid=uuid_)
        return project
    except Project.DoesNotExist:
        return None


def update_milestone(uuid=None, milestone=None, **kwargs):
    if milestone is None:
        milestone = Milestone.objects.get(uuid=uuid)
    for kw in kwargs.items():
        setattr(milestone, kw[0], kw[1])
    milestone.save()


def update_project(uuid, **kwargs):
    project = Project.objects.get(uuid=uuid)
    for kw in kwargs.items():
        setattr(project, kw[0], kw[1])
    project.save()


def get_project_attachments(project):
    project_attachments = ProjectAttachment.objects.filter(project=project).order_by('-uploaded_at')
    return project_attachments


def get_milestones(project):
    milestones = Milestone.objects.filter(project=project).order_by('created_at')
    return milestones


def get_milestone(uuid):
    milestone = Milestone.objects.get(uuid=uuid)
    return milestone


def get_project_photos(project):
    project_photos = ProjectPhoto.objects.filter(project=project)
    return project_photos
