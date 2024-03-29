# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _,  ugettext_lazy as _

from .models import Designer
from photos.utils import upload_project_photo, display_project_photo
from professionals.views import ProfessionalDetail


# TODO: add a overview database
class DesignerDetail(ProfessionalDetail):
    fields = (
        'bg_image',
        'score',
        'rank',
        'full_state_name',
        'lic_type',
        'review',
        'ratings',
        'p_lic_num',
        'project_photos',
        'review_form',
        'user_rating_form',
        'overview',
        'overview_form',
    )
    template_name = 'designer/designer.html'
    data_source = 'NCIQ'
    model_name = 'designer'

    def get_overview_message(self, **kwargs):
        message = _(
            """{bus_name} is a designer based on {city} {state} . The company holds a license number according to {data_source}. 
            The License is verified as active when we checked last time. If you would like to know {bus_name} more, 
            please contact us and we will share more information about this designer to you.
            """
        ).format(
            bus_name=kwargs.get('instance').lic_name,
            city=kwargs.get('instance').city,
            state=kwargs.get('instance').state,
            data_source=self.data_source,
            rank=kwargs.get('rank'),
            full_state_name=kwargs.get('full_state_name'),
        )
        return message


def display_project_photos(request, o_id):
    template_name = 'designer/designer_project_photo.html'
    return display_project_photo(
        request=request,
        o_id=o_id,
        model=Designer,
        template_name=template_name,
    )


def upload_project_photos(request, o_id):
    success_url = '/designer/' + o_id
    model_name = 'designer'
    template_name = 'designer/designer_project_photos_upload.html'
    return upload_project_photo(
        request=request,
        o_id=o_id,
        success_url=success_url,
        model_name=model_name,
        template_name=template_name
    )
