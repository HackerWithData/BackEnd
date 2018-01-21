# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _, ugettext_lazy as _
from django.shortcuts import render

from .models import Contractor
from .utils import (
    convert_hscore_to_rank,
    get_contractor_lic_length,
    get_bond_history,
    get_wc_history,
    get_complaint,
)
from photos.utils import upload_project_photo, display_project_photo, delete_photo
from hscore.utils import get_hscore
from professionals.views import ProfessionalDetail
from review.utils import update_accept_review as update_review


class ContractorDetail(ProfessionalDetail):
    model_name = 'contractor'
    template_name = 'contractor/contractor.html'
    data_source = 'California Contractors State License Board'

    fields = (
        'bg_image',
        'score',
        'rank',
        'length',
        'lic_type',
        'bond_history',
        'wc_history',
        'hscore',
        'score',
        'letter_grade',
        'complaint',
        'full_state_name',
        'review',
        'ratings',
        'p_id',
        'project_photos',
        'review_form',
        'user_rating_form',
        'overview',
        'overview_form',
    )

    def get_overview_message(self, **kwargs):
        message = _(
            """{lic_name} is a contractor company located in {csp} . The company holds a license number 
                    according to {data_source}. According to real-time data analysis, this licensed contractor's hoome score 
                    is {score} and is rated as {rank}. The License is verified as active when we checked last time. If you would
                     like to know {lic_name} more, please contact us and we will share more information and data about this
                      contractor to you."""
        ).format(
            lic_name=kwargs.get('instance').lic_name,
            csp=kwargs.get('instance').csp,
            data_source=self.data_source,
            score=kwargs.get('score'),
            rank=kwargs.get('letter_grade'),
            full_state_name=kwargs.get('full_state_name'),
        )
        return message

    def get_professional_length(self, **kwargs):
        return get_contractor_lic_length(kwargs.get('instance'))

    def get_professional_bond_history(self, **kwargs):
        return get_bond_history(contractor_id=kwargs.get('o_id'))

    def get_professional_wc_history(self, **kwargs):
        return get_wc_history(contractor_id=kwargs.get('o_id'))

    def get_professional_hscore(self, **kwargs):
        return get_hscore(contractor_id=kwargs.get('o_id'), contractor=kwargs.get('instance'))

    def get_professional_score(self, **kwargs):
        hscore = kwargs.get('hscore', None)
        if hscore is not None:
            return hscore.score
        else:
            return None

    def get_professional_letter_grade(self, **kwargs):
        return convert_hscore_to_rank(kwargs.get('hscore'))

    def get_professional_complaint(self, **kwargs):
        return get_complaint(contractor=kwargs.get('instance'))


def update_accept_review(request):
    update_review(request)
    return render(request, '/')


def display_project_photos(request, o_id):
    template_name = 'contractor/contractor_project_photo.html'
    return display_project_photo(
        request=request,
        o_id=o_id,
        model=Contractor,
        template_name=template_name,
    )


#TODO:
def upload_project_photos(request, o_id):
    success_url = '/contractor/' + o_id
    model_name = 'contractor'
    template_name = 'contractor/contractor_project_photos_upload.html'
    return upload_project_photo(
        request=request,
        o_id=o_id,
        success_url=success_url,
        model_name=model_name,
        template_name=template_name
    )


def del_photo(request, contractor_id):
    return delete_photo(request=request, contractor_id=contractor_id)