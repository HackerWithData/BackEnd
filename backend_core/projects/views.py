# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.contrib.auth import (logout as django_logout)

from users.models import CONSUMER, PROFESSIONAL
from users.user_helpers import get_professional_user

from .forms import (
    get_milestone_form,
    get_milestone_formset,
    get_project_form,
    get_project_edit_form,
    get_project_attachment_form,
)
from .adapter import (
    save_milestone,
    _save_milestone,
    save_project,
    save_project_photo,
    milestone_status_explanation,
)
from .decorators import check_recaptcha
from .models import (
    PAID_TO_PROFESSIONAL,
    PAYMENT_REQUEST,
)
from .utils import (
    upload_project_attachment as upload_attachment,
    get_user_projects,
    get_project,
    update_milestone,
    update_project,
    get_milestones,
    get_project_attachments,
    get_project_photos,
)
from professionals.utils import get_professional

# TODO: need to rewrite the architecture here.


@login_required
def upload_project_attachment(request, uuid):
    template_name = 'projects/upload_project_attachment.html'  # Replace with your template.
    success_url = reverse('display_project_overview') + uuid
    form = get_project_attachment_form(request=request)
    if request.method == "POST":
        project = get_project(uuid_=uuid)
        status = upload_attachment(request=request, project=project, form=form)
        if status == 'upload_success':
            return redirect(success_url)
    info_dict = {'form': form}
    return render(request, template_name, {'info_dict': info_dict})


@login_required
def upload_project_photo(request, uuid):
    template_name = 'projects/upload_project_photo.html'  # Replace with your template.
    success_url = reverse('display_project_overview') + uuid
    form = get_project_attachment_form(request)
    if request.method == "POST":
        project = get_project(uuid_=uuid)
        status = upload_attachment(request=request, project=project, form=form)
        if status == 'upload_success':
            return redirect(success_url)
    info_dict = {'form': form}
    return render(request, template_name, {'info_dict': info_dict})


@login_required
def display_project_overview(request):
    if request.method == "GET":
        template_name = 'projects/project_overview.html'
        info_dict = get_user_projects(request.user)
        return render(request, template_name, {'info_dict': info_dict})


@method_decorator(login_required, name='dispatch')
class ProjectDetail(View):
    template_name = 'projects/project_detail.html'

    def get(self, request, uuid):
        milestone_form = get_milestone_form(request)
        project = get_project(uuid_=uuid)
        if project.user is None:
            if request.user.role == CONSUMER:
                project.user = request.user
            else:
                django_logout(request)
                messages.warning(request, _("Please Login as Homeowner."))
                success_url = '/project/' + uuid
                return redirect(success_url)
        elif project.professional is None:
            if request.user.role == PROFESSIONAL:
                professional = get_professional_user(request.user)
                project.bus_name = professional.name
                project.professional = professional
            else:
                django_logout(request)
                messages.warning(request, _("Please Login as Professional."))
                success_url = '/project/' + uuid
                return redirect(success_url)
        project.save()

        project_attachments = get_project_attachments(project=project)
        project_photos = get_project_photos(project=project)
        transactions = project.transactions.all().order_by('-updated_at')
        milestones = get_milestones(project=project)
        for milestone in milestones:
            milestone.explanation = milestone_status_explanation(request, milestone.status)
        flag = False
        if request.user.role == CONSUMER:
            if request.user == project.user:
                flag = True
                professional = project.professional
        elif request.user.role == PROFESSIONAL:
            professional = request.user.professional_profiles.first().professional
            # caution
            # print(type(lic_num)) type: int
            # print(type(project.object_id)) type: unicode
            if professional == project.professional:
                flag = True
        if flag:
            info_dict = {'project': project, 'professional': professional, 'project_attachments': project_attachments,
                         'project_photos': project_photos, 'transactions': transactions,
                         'milestone_form': milestone_form, 'milestones': milestones}

            return render(request, self.template_name, {'info_dict': info_dict})
        else:
            raise Http404(_("Page Not Found"))

    def post(self, request, uuid):
        if request.POST.get('create-milestone', None):
            milestone_form = get_milestone_form(request)
            if milestone_form.is_valid():
                project = get_project(uuid_=uuid)
                # TODO: need to add this condition when this function is used in other place
                # if request.user.role == project.created_by:
                _save_milestone(milestone_form.cleaned_data['amount'], project)
                # TODO: need to consider the project status more carefully
                return redirect(request.path)

        elif request.POST.get('request-money', None):
            update_milestone(
                uuid=request.POST.get('request-money'),
                **{
                    'status': PAYMENT_REQUEST,
                }
            )
            update_project(
                uuid=uuid,
                **{
                    'project_action': "Request Money",
                }
            )
            messages.success(request, _('Success'))
            return redirect(request.path)

        elif request.POST.get('release-money', None):
            update_milestone(
                uuid=request.POST.get('release-money'),
                **{
                    'status': PAID_TO_PROFESSIONAL,
                }
            )
            update_project(
                uuid=uuid,
                **{
                    'project_action': "Release Money",
                }
            )
            # TODO: add some functions to send the money?
            messages.success(request, _('Success'))
            return redirect(request.path)

        else:  # TODO: The logic here is weird need to change
            messages.warning(request, _('Failed'))
            return redirect(request.path)  #


@check_recaptcha
def create_project(request, uuid=None):
    """
    This function is used for creating project by clicing contract us in Contractor/Designer/Architect Detail Page
    :param request:
    :param uuid:
    :return:
    """
    template_name = 'projects/project_direct_create.html'  # Replace with your template.
    direct_create = True
    professional = get_professional(uuid=uuid)
    project_form = get_project_form(
        request=request,
        uuid=uuid,
    )
    milestone_formset = get_milestone_formset(request)
    if request.method == "GET":
        if uuid:
            direct_create = False
    elif request.method == "POST":
        if request.recaptcha_is_valid and project_form.is_valid() and milestone_formset.is_valid():
            project = save_project(
                request=request,
                project_form=project_form,
                professional=professional,
            )
            save_milestone(request, project)
            upload_attachment(request=request, project=project, form=project_form)
            save_project_photo(request, project)
            success_url = reverse('display_project_overview') + project.uuid
            return redirect(success_url)
    info_dict = {
        'project_form': project_form,
        'milestone_formset': milestone_formset,
        'direct_create': direct_create,
        'professional': professional,
    }
    return render(request, template_name, {'info_dict': info_dict})


@check_recaptcha
def edit_project(request, uuid):
    template_name = "projects/edit_project.html"
    try:
        project = get_project(uuid_=uuid)
    except:
        return Http404
    project_edit_form = get_project_edit_form(request=request, project=project)
    if request.method == "POST":
        if project_edit_form.is_valid():
            project_edit_form.update(instance=project)
            success_url = reverse('display_project_detail', kwargs={'uuid': uuid})
            return redirect(success_url)
    info_dict = {'project_edit_form': project_edit_form}
    return render(request, template_name, {'info_dict': info_dict})
