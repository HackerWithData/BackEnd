# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, reverse
from forms import ProjectAttachmentForm, ProjectForm, ProjectPhotoForm
from models import ProjectAttachment, Project, ProjectPhoto
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required

import datetime


# Create your views here.
@login_required
def upload_project_attachment(request, project_id):
    template_name = 'projects/project_attachment_upload.html'  # Replace with your template.
    # TODO: Need to change sucess url.
    success_url = reverse('show_dashboard')

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
    template_name = 'projects/project_photo_upload.html'  # Replace with your template.
    # TODO: Need to change sucess url.
    success_url = reverse('show_dashboard')

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
def upload_project(request, professional_type, lic_id):
    if request.user.is_authenticated:
        template_name = 'projects/project_upload.html'  # Replace with your template.
        # TODO: Need to change success url.
        success_url = reverse('show_dashboard')

        if request.method == "POST":
            project_attachment_form = ProjectAttachmentForm(request.POST, request.FILES)
            project_form = ProjectForm(request.POST)
            project_photo_form = ProjectPhotoForm(request.POST, request.FILES)
            # project = Project.objects.get(project_id=project_id)
            if (project_attachment_form.is_valid() and project_form.is_valid()) and project_photo_form.is_valid():

                # consider another interface
                content_type = ContentType.objects.get(model=professional_type.lower())
                lic_id = int(lic_id)
                project = Project(user=request.user,
                                  first_name=project_form.cleaned_data['first_name'],
                                  last_name=project_form.cleaned_data['last_name'],
                                  content_type=content_type,
                                  object_id=lic_id,
                                  project_type=project_form.cleaned_data['project_type'],
                                  street_address=project_form.cleaned_data['street_address'],
                                  street_address2=project_form.cleaned_data['street_address2'],
                                  county=project_form.cleaned_data['county'],
                                  state=project_form.cleaned_data['state'],
                                  zipcode=project_form.cleaned_data['zipcode'],
                                  # cost=project_form.cleaned_data['cost'],
                                  start_date=project_form.cleaned_data['start_date'],
                                  # end_date=project_form.cleaned_data['end_date'],
                                  project_description=project_form.cleaned_data['project_description'],
                                  # project_status=project_form.cleaned_data['project_status']
                                  )
                #TODO:need to consider extrem scenario
                project.save()
                #attachment
                files = request.FILES.getlist('project_attachment')
                if len(files) > 0:
                    for f in files:
                        instance = ProjectAttachment.objects.create(project_attachment=f, title=f.name, project=project,
                                                                    attachment_type=project_attachment_form.cleaned_data['attachment_type'])
                        instance.save()
                else:
                    pass
                #photos
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
                                                'start_date': datetime.datetime.today().strftime('%Y-%m-%d')})
        else:
            project_form = ProjectForm(initial={'first_name': request.user.first_name,
                                                'last_name': request.user.last_name,
                                                'start_date': datetime.datetime.today().strftime('%Y-%m-%d')})
        project_attachment_form = ProjectAttachmentForm()
        project_photo_form = ProjectPhotoForm()
        info_dict = {'project_form': project_form, 'project_attachment_form': project_attachment_form,
                     'project_photo_form': project_photo_form}
        return render(request, template_name, {'info_dict': info_dict})
    else:
        return HttpResponseNotFound("Sorry. Pages Not Found")
