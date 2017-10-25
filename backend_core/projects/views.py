# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, reverse
from forms import ProjectAttachmentForm, ProjectForm, ProjectPhotoForm
from models import Project, ProjectPhoto, ProjectAttachment
# from transactions.models import Transaction
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
import datetime
from django.conf import settings
from django.contrib import messages
from decorators import check_recaptcha
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator


# Create your views here.
@login_required
def upload_project_attachment(request, project_id):
    template_name = 'projects/upload_project_attachment.html'  # Replace with your template.
    success_url = reverse('display_project_overview')

    if request.method == "POST":
        form = ProjectAttachmentForm(request.POST, request.FILES)
        project = Project.objects.get(project_id=project_id)
        files = request.FILES.getlist('project_attachment')
        if form.is_valid():
            if len(files) > 0:
                for f in files:
                    instance = ProjectAttachment.objects.create(file=f, title=f.name, project=project,
                                                                attachment_type=form.attachment_type)
                    instance.save()
            else:
                pass
            return redirect(success_url)
    form = ProjectAttachmentForm()
    info_dict = {'form': form}
    return render(request, template_name, info_dict)


@login_required
def upload_project_photo(request, project_id):
    template_name = 'projects/upload_project_photo.html'  # Replace with your template.
    success_url = reverse('display_project_overview')

    if request.method == "POST":
        form = ProjectAttachmentForm(request.POST, request.FILES)
        project = Project.objects.get(project_id=project_id)
        files = request.FILES.getlist('project_photo')
        if form.is_valid():
            if len(files) > 0:
                for f in files:
                    instance = ProjectAttachment.objects.create(file=f, title=f.name, project=project)
                    instance.save()
            else:
                pass
            return redirect(success_url)
    form = ProjectAttachmentForm()
    info_dict = {'form': form}
    return render(request, template_name, info_dict)


@login_required
@check_recaptcha
def create_project(request, professional_type, lic_id):
    if request.user.is_authenticated and request.user.role == "CONSUMER":
        template_name = 'projects/create_project.html'  # Replace with your template.
        success_url = reverse('display_project_overview')

        if request.method == "POST":
            project_form = ProjectForm(request.POST, request.FILES)
            # project = Project.objects.get(project_id=project_id)
            if project_form.is_valid() and request.recaptcha_is_valid:

                # consider another interface
                content_type = ContentType.objects.get(model=professional_type.lower())
                lic_id = int(lic_id)
                professional = content_type.objects.get_object_for_this_type(pk=lic_id)
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
                                  # project_status=project_form.cleaned_data['project_status']
                                  )
                # TODO:need to consider extrem scenario
                project.save()
                # attachment
                files = request.FILES.getlist('project_attachment')
                if len(files) > 0:
                    for f in files:
                        instance = ProjectAttachment.objects.create(project_attachment=f, title=f.name, project=project,
                                                                    attachment_type=project_form.cleaned_data[
                                                                        'attachment_type'])
                        instance.save()
                else:
                    pass
                # photos
                files = request.FILES.getlist('project_photo')
                if len(files) > 0:
                    for f in files:
                        instance = ProjectPhoto.objects.create(project_photo=f, title=f.name, project=project)
                        instance.save()
                else:
                    pass

                return redirect(success_url)
        # TODO: consider another interface
        if request.user.is_authenticated:
            project_form = ProjectForm(initial={'first_name': request.user.first_name,
                                                'last_name': request.user.last_name,
                                                'start_date': datetime.datetime.today()})
        else:
            project_form = ProjectForm(initial={'first_name': request.user.first_name,
                                                'last_name': request.user.last_name,
                                                'start_date': datetime.datetime.today()})

        info_dict = {'project_form': project_form}
        return render(request, template_name, {'info_dict': info_dict})
    else:
        return HttpResponseNotFound("Sorry. Pages Not Found")


@login_required
def display_project_overview(request):
    template_name = 'projects/project_overview.html'
    if request.user.role == "CONSUMER":
        projects = Project.objects.filter(user=request.user).order_by('-project_id')
        info_dict = {'projects': projects}
    elif request.user.role == 'PROFESSIONAL':
        professional = request.user.professional_profiles.first().professional
        projects = Project.objects.filter(
            conternt_type=professional.type.lower(),
            object_id=int(professional.professional.lic_num)).order_by('-project_id')
        info_dict = {'projects': projects, 'professional': professional}
    return render(request, template_name, {'info_dict': info_dict})


@method_decorator(login_required, name='dispatch')
class ProjectDetail(TemplateView):
    template_name = 'projects/project_detail.html'

    def get(self, request, project_id):
        project = Project.objects.get(project_id=project_id)
        project_attachments = ProjectAttachment.objects.filter(project=project).order_by('-uploaded_at')
        project_photos = ProjectPhoto.objects.filter(project=project)
        transactions = project.transactions.all().order_by('-updated_at')
        # print(transactions)
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
                         'content_type': str(project.content_type)}

            return render(request, self.template_name, {'info_dict': info_dict})
        else:
            return HttpResponseNotFound("Page Not Found")

    def post(self, request, project_id):

        if request.POST.get('request-money'):
            project = Project.objects.get(project_id=project_id)
            project.project_status = "P"
            project.project_action = "Request for Payment to move on"
            project.save()

            messages.success(request, 'Request Success')
            return redirect(request.path)
        else:
            messages.warning(request, 'Request Failed')
        # if flag:
        #     info_dict = {'project': project, 'professional': professional,
        #                  'project_attachments': project_attachments,
        #                  'project_photos': project_photos, 'transactions': transactions,
        #                  'content_type': str(project.content_type)}
        #     raise messages("Request Sucess")
        #     return render(request, self.template_name, {'info_dict': info_dict})
        # else:
        #     return HttpResponseNotFound("Page Not Found")
