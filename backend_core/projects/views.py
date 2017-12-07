# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, reverse
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as __, ugettext as _

from .decorators import check_recaptcha
from .forms import ProjectAttachmentForm, ProjectForm, ProjectPhotoForm, MilestoneForm, ProjectFormDirectCreate
from .models import Project, ProjectPhoto, ProjectAttachment, Milestone
from .utils import get_a_uuid, WAITING, PENDING, PAID_TO_PROFESSIONAL, PAYMENT_REQUEST, PAID_TO_HOOME
from users.utils import CONSUMER, PROFESSIONAL
from users.user_helpers import get_professional_user, get_user_by_hoome_id


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


# TODO: need to rewrite the architecture here.
# Create your views here.
@login_required
def upload_project_attachment(request, uuid):
    template_name = 'projects/upload_project_attachment.html'  # Replace with your template.
    success_url = reverse('display_project_overview') + uuid

    if request.method == "POST":
        form = ProjectAttachmentForm(request.POST, request.FILES)
        project = Project.objects.get(uuid=uuid)
        files = request.FILES.getlist('project_attachment')
        if form.is_valid():
            if len(files) > 0:
                for f in files:
                    ProjectAttachment.objects.create(file=f, title=f.name, project=project,
                                                     attachment_type=form.attachment_type)
            else:
                pass
            return redirect(success_url)
    form = ProjectAttachmentForm()
    info_dict = {'form': form}
    return render(request, template_name, {info_dict: 'info_dict'})


@login_required
def upload_project_photo(request, uuid):
    template_name = 'projects/upload_project_photo.html'  # Replace with your template.
    success_url = reverse('display_project_overview') + uuid

    if request.method == "POST":
        form = ProjectAttachmentForm(request.POST, request.FILES)
        project = Project.objects.get(uuid=uuid)
        files = request.FILES.getlist('project_photo')
        if form.is_valid():
            if len(files) > 0:
                for f in files:
                    ProjectAttachment.objects.create(file=f, title=f.name, project=project)
            else:
                pass
            return redirect(success_url)
    form = ProjectPhotoForm()
    info_dict = {'form': form}
    return render(request, template_name, {info_dict: 'info_dict'})


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


@login_required
@check_recaptcha
def create_project(request, professional_type, lic_id):
    """
    This function is used for creating project by clicing contract us in Contractor/Designer/Architect Detail Page
    :param request:
    :param professional_type:
    :param lic_id:
    :return:
    """
    if request.user.is_authenticated and request.user.role == CONSUMER:
        template_name = 'projects/create_project.html'  # Replace with your template.
        if request.method == "POST":
            project_form = ProjectForm(request.POST, request.FILES)
            # project = Project.objects.get(project_id=project_id)
            if project_form.is_valid() and request.recaptcha_is_valid:
                content_type = ContentType.objects.get(model=professional_type.lower())
                lic_id = int(lic_id)
                professional = content_type.get_object_for_this_type(pk=lic_id)
                project = project_form.save_project(commit=False)
                project.user = request.user
                project.content_type = content_type
                project.object_id = lic_id
                project.bus_name = professional.lic_name
                project.save()
                save_project_attachment(request, project, project_form)
                save_project_photo(request, project)
                success_url = reverse('display_project_overview') + project.uuid
                return redirect(success_url)
        else:
            pass

        project_form = ProjectForm(initial={'first_name': request.user.first_name,
                                            'last_name': request.user.last_name,
                                            'start_date': datetime.datetime.today()})
        info_dict = {'project_form': project_form}
        return render(request, template_name, {'info_dict': info_dict})
    else:
        messages.warning(request, __('Please Log in as Homeowner first.'))
        return redirect(request.path)


@login_required
def display_project_overview(request):
    # print(vars(request))
    if request.method == "GET":
        template_name = 'projects/project_overview.html'
        if request.user.role == CONSUMER:
            projects = Project.objects.filter(user=request.user).order_by('-project_id')
            info_dict = {'projects': projects}
        elif request.user.role == PROFESSIONAL:
            professional = request.user.professional_profiles.first().professional
            projects = Project.objects.filter(content_type=ContentType.objects.get(model=professional.type.lower()),
                                              object_id=int(professional.lic_num)).order_by('-project_id')
            info_dict = {'projects': projects, 'professional': professional}
        return render(request, template_name, {'info_dict': info_dict})


@method_decorator(login_required, name='dispatch')
class ProjectDetail(View):
    template_name = 'projects/project_detail.html'

    def get(self, request, uuid):
        initial = {
            "amount": 2000
        }
        milestone_form = MilestoneForm(initial=initial)
        project = Project.objects.get(uuid=uuid)
        if project.user is None:
            project.user = request.user
            project.save()
        elif project.content_type is None:
            pro = get_professional_user(request.user)
            project.content_type = ContentType.objects.get(model=pro.type.lower())
            project.object_id = pro.lic_num
            project.save()
        project_attachments = ProjectAttachment.objects.filter(project=project).order_by('-uploaded_at')
        project_photos = ProjectPhoto.objects.filter(project=project)
        transactions = project.transactions.all().order_by('-updated_at')
        milestones = Milestone.objects.filter(project=project).order_by('created_at')
        if milestones.count > 0:
            for milestone in milestones:
                milestone.explanation = milestone_status_explanation(request, milestone.status)
        flag = False
        if request.user.role == CONSUMER:
            if request.user == project.user:
                flag = True
                professional = project.content_type.get_object_for_this_type(pk=project.object_id)
        elif request.user.role == PROFESSIONAL:
            professional = request.user.professional_profiles.first().professional
            ct = ContentType.objects.get(model=professional.type.lower())
            lic_num = ct.get_object_for_this_type(lic_num=professional.lic_num).pk
            # caution
            # print(type(lic_num)) type: int
            # print(type(project.object_id)) type: unicode
            if ct == project.content_type and str(lic_num) == str(project.object_id):
                flag = True

        if flag:
            info_dict = {'project': project, 'professional': professional, 'project_attachments': project_attachments,
                         'project_photos': project_photos, 'transactions': transactions,
                         'milestone_form': milestone_form, 'milestones': milestones,
                         'content_type': str(project.content_type)}

            return render(request, self.template_name, {'info_dict': info_dict})
        else:
            raise Http404(__("Page Not Found"))

    def post(self, request, uuid):
        if request.POST.get('create-milestone'):
            milestone_form = MilestoneForm(request.POST)
            # print(milestone_form.is_valid())
            if milestone_form.is_valid():

                project = Project.objects.get(uuid=uuid)
                # TODO: need to add this condition when this function is used in other place
                # if request.user.role == project.created_by:
                flag = True
                while flag:
                    try:
                        milestone_uuid = get_a_uuid()
                        Milestone.objects.get(uuid=milestone_uuid)
                    except Milestone.DoesNotExist:
                        flag = False
                Milestone.objects.create(amount=milestone_form.cleaned_data['amount'], project=project,
                                         uuid=milestone_uuid)

                # TODO: need to consider the project status more carefully
                # project.project_status = PENDING
                # project.project_action = "."
                # project.save()
                return redirect(request.path)

        elif request.POST.get('request-money'):
            # print(request.POST)
            # print(request.POST.get('request-money'))

            milestone = Milestone.objects.get(uuid=request.POST.get('request-money'))
            milestone.status = PAYMENT_REQUEST
            milestone.save()
            project = Project.objects.get(uuid=uuid)
            project.project_action = "Request Money"
            # The professional requests homeowner to allow Hoome release the payment and make a new payment for next milestone.
            project.save()
            messages.success(request, __('Success'))
            return redirect(request.path)

        elif request.POST.get('release-money'):
            milestone = Milestone.objects.get(uuid=request.POST.get('release-money'))
            milestone.status = PAID_TO_PROFESSIONAL
            milestone.save()
            project = Project.objects.get(uuid=uuid)
            project.project_action = "Release Money"
            # TODO: add some functions to send the money?
            project.save()
            messages.success(request, __('Success'))
            return redirect(request.path)

        else:  # TODO: The logic here is weird need to change
            messages.warning(request, __('Failed'))
            return redirect(request.path)  #


def save_project(request, project_form):
    project = project_form.save_project(commit=False)
    # pro means the professional in Professional model
    if project_form.cleaned_data['created_by'] == CONSUMER:
        pro = get_professional_user(get_user_by_hoome_id(project_form.cleaned_data['professional_hoome_id']))
        project.content_type = ContentType.objects.get(model=pro.type.lower())
        project.object_id = pro.lic_num
        project.bus_name = pro.name
        if request.user.is_authenticated:  # when user is logged in
            project.user = request.user

    elif project_form.cleaned_data['created_by'] == PROFESSIONAL:
        project.user = get_user_by_hoome_id(project_form.cleaned_data['homeowner_hoome_id'])
        if request.user.is_authenticated:  # when user is logged in
            pro = get_professional_user(request.user)
            project.content_type = ContentType.objects.get(model=pro.type.lower())
            project.object_id = pro.lic_num
            project.bus_name = pro.name

    project.save()
    return project


@check_recaptcha
def create_project_direct(request):
    template_name = 'projects/project_direct_create.html'  # Replace with your template.

    if request.method == "GET":
        # initial={'start_date': datetime.datetime.today()}
        project_form = ProjectFormDirectCreate()
        info_dict = {'project_form': project_form}
        return render(request, template_name, {'info_dict': info_dict})
    elif request.method == "POST":
        project_form = ProjectFormDirectCreate(request.POST, request.FILES)
        if project_form.is_valid() and request.recaptcha_is_valid:
            project = save_project(request, project_form)
            save_project_attachment(request, project, project_form)
            save_project_photo(request, project)
            success_url = reverse('display_project_overview') + project.uuid
            request.session['success_url'] = success_url
            return redirect(success_url)
        else:
            info_dict = {'project_form': project_form}
            return render(request, template_name, {'info_dict': info_dict})
