# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, reverse
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.forms.formsets import formset_factory
from django.contrib.auth import (logout as django_logout)
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from users.utils import CONSUMER, PROFESSIONAL
from users.user_helpers import get_professional_user, get_user_by_hoome_id

from .forms import ProjectAttachmentForm, ProjectForm, ProjectFormDirectCreate, ProjectPhotoForm, MilestoneForm
from .adapter import save_milestone, _save_milestone, save_project, save_project_attachment, save_project_photo, \
    milestone_status_explanation
from .decorators import check_recaptcha
from .forms import ProjectAttachmentForm, ProjectForm, ProjectPhotoForm, MilestoneForm, ProjectFormDirectCreate, \
    ProjectEditForm
from .models import Project, ProjectPhoto, ProjectAttachment, Milestone
from .utils import get_a_uuid, WAITING, PENDING, PAID_TO_PROFESSIONAL, PAYMENT_REQUEST, PAID_TO_HOOME
from helplers import validate_hoome_id

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


@login_required
def display_project_overview(request):
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
        initial = {"amount": 2000}
        milestone_form = MilestoneForm(initial=initial)
        project = Project.objects.get(uuid=uuid)

        if project.user is None:
            if request.user.role == CONSUMER:
                project.user = request.user
            else:
                django_logout(request)
                messages.warning(request, _("Please Login as Homeowner."))
                request.session['success_url'] = '/project/' + uuid
                return redirect(request.session['success_url'])
        elif project.content_type is None:
            if request.user.role == PROFESSIONAL:
                pro = get_professional_user(request.user)
                project.bus_name = pro.name
                project.content_type = ContentType.objects.get(model=pro.type.lower())
                project.object_id = pro.lic_num
            else:
                django_logout(request)
                messages.warning(request, _("Please Login as Professional."))
                request.session['success_url'] = '/project/' + uuid
                return redirect(request.session['success_url'])
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
            raise Http404(_("Page Not Found"))

    def post(self, request, uuid):
        if request.POST.get('create-milestone'):
            milestone_form = MilestoneForm(request.POST)
            # print(milestone_form.is_valid())
            if milestone_form.is_valid():
                project = Project.objects.get(uuid=uuid)
                # TODO: need to add this condition when this function is used in other place
                # if request.user.role == project.created_by:
                _save_milestone(milestone_form.cleaned_data['amount'], project)
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
            project.save()

            # The professional requests homeowner to allow Hoome release the payment and make a new payment for next milestone.
            messages.success(request, _('Success'))
            return redirect(request.path)

        elif request.POST.get('release-money'):
            milestone = Milestone.objects.get(uuid=request.POST.get('release-money'))
            milestone.status = PAID_TO_PROFESSIONAL
            milestone.save()
            project = Project.objects.get(uuid=uuid)
            project.project_action = "Release Money"
            project.save()
            # TODO: add some functions to send the money?
            messages.success(request, _('Success'))
            return redirect(request.path)

        else:  # TODO: The logic here is weird need to change
            messages.warning(request, _('Failed'))
            return redirect(request.path)  #


# else:
#     messages.warning(request, _('Please Log in as Homeowner first.'))
#     django_logout(request)
#     return redirect(reverse('account_login')+'?next='+request.path)
@check_recaptcha
def create_project(request, professional_type=None, lic_id=None):
    """
    This function is used for creating project by clicing contract us in Contractor/Designer/Architect Detail Page
    :param request:
    :param professional_type:
    :param lic_id:
    :return:
    """
    template_name = 'projects/project_direct_create.html'  # Replace with your template.
    direct_create = True
    MilestoneFormSet = formset_factory(MilestoneForm)
    if request.method == "GET":
        # initial={'start_date': datetime.datetime.today()}
        milestone_formset = MilestoneFormSet()
        if professional_type and lic_id:
            if request.user.is_authenticated:
                project_form = ProjectForm(initial={'first_name': request.user.first_name,
                                                    'last_name': request.user.last_name})
            else:
                project_form = ProjectForm()
        else:
            project_form = ProjectFormDirectCreate()
        if professional_type and lic_id:
            direct_create = False

    elif request.method == "POST":
        # print(request.POST)
        if professional_type and lic_id:
            project_form = ProjectForm(request.POST, request.FILES)
        else:
            project_form = ProjectFormDirectCreate(request.POST, request.FILES)
        milestone_formset = MilestoneFormSet(request.POST)

        if request.recaptcha_is_valid and project_form.is_valid() and milestone_formset.is_valid():
            # print(request.POST)
            # print(milestone_formset)
            project = save_project(request, project_form, professional_type, lic_id)
            save_milestone(request, project)
            save_project_attachment(request, project, project_form)
            save_project_photo(request, project)
            success_url = reverse('display_project_overview') + project.uuid
            request.session['success_url'] = success_url
            return redirect(success_url)

    info_dict = {'project_form': project_form, 'milestone_formset': milestone_formset, 'direct_create': direct_create}
    return render(request, template_name, {'info_dict': info_dict})


@check_recaptcha
def edit_project(request, uuid):
    template_name = "projects/edit_project.html"
    project = get_object_or_404(Project, uuid=uuid)
    if request.method == "GET":
        project_edit_form = ProjectEditForm(initial=model_to_dict(project))
    elif request.method == "POST":
        project_edit_form = ProjectEditForm(request.POST)
        if project_edit_form.is_valid():
            project_edit_form.update(instance=project)
            success_url = reverse('display_project_detail', kwargs={'uuid': uuid})
            return redirect(success_url)
    info_dict = {'project_edit_form': project_edit_form}
    return render(request, template_name, {'info_dict': info_dict})
