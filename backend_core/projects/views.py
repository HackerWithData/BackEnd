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
from django.utils.translation import ugettext_lazy as _

from .decorators import check_recaptcha
from .utils import get_a_uuid, WAITING, PENDING, PAYED_TO_CONTRACTOR
from .forms import ProjectAttachmentForm, ProjectForm, ProjectPhotoForm, MilestoneForm
from .models import Project, ProjectPhoto, ProjectAttachment, Milestone


# TODO: need to rewrite the architecture here.
# Create your views here.
@login_required
def upload_project_attachment(request, project_uuid):
    template_name = 'projects/upload_project_attachment.html'  # Replace with your template.
    success_url = reverse('display_project_overview') + project_uuid

    if request.method == "POST":
        form = ProjectAttachmentForm(request.POST, request.FILES)
        project = Project.objects.get(project_uuid=project_uuid)
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
def upload_project_photo(request, project_uuid):
    template_name = 'projects/upload_project_photo.html'  # Replace with your template.
    success_url = reverse('display_project_overview') + project_uuid

    if request.method == "POST":
        form = ProjectAttachmentForm(request.POST, request.FILES)
        project = Project.objects.get(project_uuid=project_uuid)
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
@check_recaptcha
def create_project(request, professional_type, lic_id):
    if request.user.is_authenticated:
        template_name = 'projects/create_project.html'  # Replace with your template.
        success_url = reverse('display_project_overview')

        if request.method == "POST" and request.user.role == "CONSUMER":
            project_form = ProjectForm(request.POST, request.FILES)
            # project = Project.objects.get(project_id=project_id)
            if project_form.is_valid() and request.recaptcha_is_valid:
                # TODO: consider another interface
                content_type = ContentType.objects.get(model=professional_type.lower())
                lic_id = int(lic_id)
                professional = content_type.get_object_for_this_type(pk=lic_id)

                flag = True
                while flag:
                    try:
                        project_uuid = get_a_uuid()
                        Project.objects.get(project_uuid=project_uuid)
                    except Project.DoesNotExist:
                        flag = False
                # TODO this step can be simplified to form.save()
                project = Project(user=request.user,
                                  project_name=project_form.cleaned_data['project_name'],
                                  first_name=project_form.cleaned_data['first_name'],
                                  last_name=project_form.cleaned_data['last_name'],
                                  content_type=content_type,
                                  object_id=lic_id,
                                  bus_name=professional.lic_name,
                                  project_type=project_form.cleaned_data['project_type'],
                                  street_address=project_form.cleaned_data['street_address'],
                                  street_address2=project_form.cleaned_data['street_address2'],
                                  county=project_form.cleaned_data['county'],
                                  state=project_form.cleaned_data['state'],
                                  zipcode=project_form.cleaned_data['zipcode'],
                                  # country=project_form.cleaned_data['country'],
                                  # cost=project_form.cleaned_data['project_cost'],
                                  start_date=project_form.cleaned_data['start_date'],
                                  # end_date=project_form.cleaned_data['end_date'],
                                  project_description=project_form.cleaned_data['project_description'],
                                  project_status=WAITING,
                                  project_uuid=project_uuid)
                # TODO:need to consider extreme scenario
                project.save()
                # attachment
                files = request.FILES.getlist('project_attachment')
                if len(files) > 0:
                    for f in files:
                        ProjectAttachment.objects.create(project_attachment=f, title=f.name, project=project,
                                                         attachment_type=project_form.cleaned_data['attachment_type'])
                else:
                    pass
                # photos
                files = request.FILES.getlist('project_photo')
                if len(files) > 0:
                    for f in files:
                        ProjectPhoto.objects.create(project_photo=f, title=f.name, project=project)
                else:
                    pass

                return redirect(success_url)
        else:
            # TODO: what if role != consumer
            pass
        # TODO: consider another interface
        # if request.user.is_authenticated:
        project_form = ProjectForm(initial={'first_name': request.user.first_name,
                                            'last_name': request.user.last_name,
                                            'start_date': datetime.datetime.today()})
        # else:
        #     project_form = ProjectForm(initial={'first_name': request.user.first_name,
        #                                         'last_name': request.user.last_name,
        #                                         'start_date': datetime.datetime.today()})

        info_dict = {'project_form': project_form}
        return render(request, template_name, {'info_dict': info_dict})
    else:
        messages.warning(request, _('Please Log in first.'))
        return redirect(request.path)


@login_required
def display_project_overview(request):
    template_name = 'projects/project_overview.html'
    if request.user.role == "CONSUMER":
        projects = Project.objects.filter(user=request.user).order_by('-project_id')
        info_dict = {'projects': projects}
    elif request.user.role == 'PROFESSIONAL':
        professional = request.user.professional_profiles.first().professional
        projects = Project.objects.filter(content_type=ContentType.objects.get(model=professional.type.lower()),
                                          object_id=int(professional.lic_num)).order_by('-project_id')
        info_dict = {'projects': projects, 'professional': professional}
    return render(request, template_name, {'info_dict': info_dict})


@method_decorator(login_required, name='dispatch')
class ProjectDetail(View):
    template_name = 'projects/project_detail.html'

    def get(self, request, project_uuid):
        initial = {
            "amount": 0
        }
        milestone_form = MilestoneForm(initial=initial)
        project = Project.objects.get(project_uuid=project_uuid)
        project_attachments = ProjectAttachment.objects.filter(project=project).order_by('-uploaded_at')
        project_photos = ProjectPhoto.objects.filter(project=project)
        transactions = project.transactions.all().order_by('-updated_at')
        milestones = Milestone.objects.filter(project=project).order_by('created_at')

        flag = False
        if request.user.role == "CONSUMER":
            if request.user == project.user:
                flag = True
                professional = project.content_type.get_object_for_this_type(pk=project.object_id)
        elif request.user.role == "PROFESSIONAL":
            professional = request.user.professional_profiles.first().professional
            ct = ContentType.objects.get(model=professional.type.lower())
            lic_num = ct.get_object_for_this_type(lic_num=professional.lic_num)
            if ct == project.content_type and lic_num == project.object_id:
                flag = True

        if flag:
            info_dict = {'project': project, 'professional': professional, 'project_attachments': project_attachments,
                         'project_photos': project_photos, 'transactions': transactions,
                         'milestone_form': milestone_form, 'milestones': milestones,
                         'content_type': str(project.content_type)}

            return render(request, self.template_name, {'info_dict': info_dict})
        else:
            raise Http404(_("Page Not Found"))

    def post(self, request, project_uuid):
        if request.POST.get('create-milestone'):
            milestone_form = MilestoneForm(request.POST)
            print(milestone_form.is_valid())
            if milestone_form.is_valid():

                project = Project.objects.get(project_uuid=project_uuid)
                flag = True
                while flag:
                    try:
                        milestone_uuid = get_a_uuid()
                        Milestone.objects.get(milestone_uuid=milestone_uuid)
                    except Milestone.DoesNotExist:
                        flag = False
                milestone = Milestone(amount=milestone_form.cleaned_data['amount'], project=project,
                                      milestone_uuid=milestone_uuid)
                # TODO: need to add milestone status here
                milestone.save()
                project.project_status = PENDING
                project.project_action = "."
                project.save()
                return redirect(request.path)

        elif request.POST.get('request-money'):
            try:
                project = Project.objects.get(project_uuid=project_uuid)
                project.project_status = PENDING
                project.project_action = "Current Milestone is done."
                # The professional requests homeowner to allow Hoome release the payment and make a new payment for next milestone.
                project.save()
                messages.success(request, _('Success'))
                return redirect(request.path)
            except:
                # TODO: The logic here is weird need to change
                messages.warning(request, _('Failed'))
                return redirect(request.path)

        elif request.POST.get('release-money'):
            try:
                project = Project.objects.get(project_uuid=project_uuid)
                project.project_status = PAYED_TO_CONTRACTOR
                project.project_action = "Current Milestone is done."
                # TODO: add some functions to send the money?
                project.save()
                messages.success(request, _('Success'))
                return redirect(request.path)
            except:
                # TODO: The logic here is weird need to change
                messages.warning(request, _('Failed'))
                return redirect(request.path)

#
# @method_decorator(login_required, name='dispatch')
# class Milestone(View):
#
#
#     def get(self):
#
#     def post(self):
#
