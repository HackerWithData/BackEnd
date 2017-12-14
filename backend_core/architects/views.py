# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Architect
from professionals.views import ProfessionalDetail


# TODO: add a overview database
class ArchitectDetail(ProfessionalDetail):

    def __init__(self):
        super(ArchitectDetail, self).__init__()
        self.model = Architect
        self.data_source = 'California Architects Board'
        self.template_name = 'architect/architect.html'


def display_project_photos(request, o_id):
    return display_project_photo(request, o_id, Architect)


def upload_project_photos(request, o_id):
    success_url = '/architect/' + o_id
    model_name = 'architect'
    return upload_project_photo(
        request=request,
        o_id=o_id,
        success_url=success_url,
        model_name=model_name,
    )
