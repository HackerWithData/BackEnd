# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _,  ugettext_lazy as _

from .models import Meister
from professionals.views import ProfessionalDetail
from photos.utils import upload_project_photo, display_project_photo
from review.utils import update_accept_review as update_review


class MeisterDetail(ProfessionalDetail):
    template_name = 'meister/meister.html'
    model_name = 'meister'
    data_source = 'California Contractors State License Board'

    fields = (
        'bgimage',
        'score',
        'rank',
        'full_state_name',
        'review',
        'ratings',
        'p_lic_num',
        'project_photos',
        'review_form',
        'user_rating_form',
        'overview',
        'overview_form',
    )

    def get_overview_message(self, **kwargs):
        message = _(
            """{lic_name} is a professional located in {full_state_name}. The professional is verified as 
        active when we checked last time. If you would like to know {lic_name} more, please contact us and we will 
        share more information and data about this meister to you."""
        ).format(
            lic_name=kwargs.get('instance').lic_name,
            full_state_name=kwargs.get('full_state_name'),
        )
        return message


#TODO: this function is derecated. Jeremy will revise this part and make it reuseable.
def update_accept_review(request):
    update_review(request)
    return render(request, '/')


def display_project_photos(request, o_id):
    template_name = 'meister/meister_project_photo.html'
    return display_project_photo(
        request=request,
        o_id=o_id,
        model=Designer,
        template_name=template_name,
    )


def upload_project_photos(request, o_id):
    success_url = '/meister/' + o_id
    model_name = 'meister'
    template_name = 'meister/meister_project_photos_upload.html'
    return upload_project_photo(
        request=request,
        o_id=o_id,
        success_url=success_url,
        model_name=model_name,
        template_name=template_name
    )