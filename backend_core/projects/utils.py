import uuid
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from .models import ProjectAttachment, Project, Milestone
from users.utils import CONSUMER, PROFESSIONAL


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


def upload_project_attachment(request, uuid):
    form = ProjectAttachmentForm(request.POST, request.FILES)
    project = Project.objects.get(uuid=uuid)
    files = request.FILES.getlist('project_attachment')
    if form.is_valid():
        for f in files:
            ProjectAttachment.objects.create(
                file=f,
                title=f.name,
                project=project,
                attachment_type=form.attachment_type,
            )
        return 'upload_success'
    return 'form_error'


def get_user_projects(user):
    if user.role == CONSUMER:
        projects = Project.objects.filter(user=user).order_by('-project_id')
        info_dict = {'projects': projects}
    elif user.role == PROFESSIONAL:
        professional = user.professional_profiles.first().professional
        projects = Project.objects.filter(
            content_type=ContentType.objects.get(model=professional.type.lower()),
            object_id=int(professional.lic_num)
        ).order_by('-project_id')
        info_dict = {'projects': projects, 'professional': professional}
    return info_dict


def get_milestone(initial={'amount': 2000}):
    milestone_form = MilestoneForm(initial={'amount': 2000})
    return milestone_form


def get_project(uuid):
    project = Project.objects.get(uuid=uuid)
    return project


def update_milestone(uuid, **kwargs):
    milestone = Milestone.objects.get(uuid=uuid)
    for kw in kwargs:
        setattr(milestone, kw[0], kw[1])
    milestone.save()


def update_project(uuid, **kwargs):
    project = Project.objects.get(uuid=uuid)
    for kw in kwargs:
        setattr(project, kw[0], kw[1])
    project.save()