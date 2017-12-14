# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseNotFound, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _, ugettext_lazy as _
from django.views import View

from models import Contractor
from utils import convert_hscore_to_rank, get_state_full_name, avg_rating

# from review.utils import (
#     get_review,
#     get_review_form,
#     post_review,
#     get_p_lic_num,
# )

from photos.utils import (
    get_background_photo,
    get_project_photos,
    display_project_photo,
    upload_project_photo,
    delete_photo,
)

# from overviews.views import edit_overview

from contractors.utils import (
    get_state_full_name,
    get_bond_history,
    get_workcompensation_history,
    get_complaint,
)

# from ratings.utils import (
#     RATING_STAR_MAX,
#     get_rating,
#     get_user_rating_form,
# )

from overviews.utils import (
    get_overview,
    get_overview_form,
)

from hscore.utils import get_hscore
from professionals.views import ProfessionalDetail


class ContractorDetail(ProfessionalDetail):
    def __init__(self):
        super(ContractorDetail, self).__init__()
        self.model = Contractor
        self.data_source = 'California Contractors State License Board'
        self.template_name = 'contractor/contractor.html'

    def get_contractor_lic_length(self, contractor):
        if (contractor.lic_expire_date is not None) and (contractor.lic_expire_date < datetime.date.today()):
            length = int(contractor.lic_expire_date.year - contractor.lic_issue_date.year)
        # test issue, won't happen in prod
        elif (not contractor.lic_expire_date) and (not contractor.lic_issue_date):
            length = 0
        else:
            length = int(datetime.date.today().year - contractor.lic_issue_date.year)
        return length

    def get_professional_overview(self, request, o_id, instance):
        model_name = str(ContentType.objects.get_for_model(instance).name)
        data_source = self.data_source
        hscore = get_hscore(contractor_id=o_id)
        full_state_name = get_state_full_name(instance.state)
        letter_grade = convert_hscore_to_rank(hscore)

        overview = get_overview(
                    model_name=model_name,
                    object_id=o_id,
                    **{
                        'bus_name': instance.lic_name,
                        'city': instance.csp,
                        'data_source': data_source,
                        'score': hscore.score,
                        'rank': letter_grade,
                        'full_state_name': full_state_name,
                    }
                )
        return overview

    def get_info_dict(self, request, o_id):
        super(ContractorDetail, self).get_info_dict(request, o_id)
        info_dict = self.info_dict
        bh = get_bond_history(contractor_id=o_id)
        wh = get_workcompensation_history(contractor_id=o_id)
        hscore = get_hscore(contractor_id=o_id)
        letter_grade = convert_hscore_to_rank(hscore)
        complaint = get_complaint(contractor=contractor)
        length = self.get_contractor_lic_length(contractor=contractor)
        info_dict.update(
            {
                'bh': bh,
                'wh': wh,
                'hscore': hscore,
                'letter_grade': letter_grade,
                'complaint': complaint,
                'length': length,
            }
        )


def update_accept_review(request):
    review = Review.objects.get(contractor=request.contractor)
    review.review_status = 'A'
    review.save()
    ur = UserRating.objects.get(review=review)
    for r in ur:
        rating = Rating.objects.get(contractor=request.contractor, rating_type=review.rating_type)
        rating.total = rating.total + r.rating_score
        rating.count = rating.count + 1
        rating.average = round(rating.total * 1.0 / rating.count, 2)
    return render(request, '/')


def display_project_photos(request, contractor_id):
    return display_project_photo(request=request, o_id=contractor_id, model=Contractor)


def upload_project_photos(request, contractor_id):
    success_url = '/contractor/' + o_id
    model_name = 'contractor'
    return upload_project_photo(
        request=request,
        o_id=o_id,
        success_url=success_url,
        model_name=model_name,
    )


def del_photo(request, contractor_id):
    return deletes_photo(request=request, contractor_id=contractor_id)