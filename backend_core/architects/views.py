# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.
import datetime
from django.utils.translation import ugettext as _,  ugettext_lazy as _
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.contenttypes.models import ContentType

from review.utils import (
    get_review,
    get_review_form,
    post_review,
    get_p_lic_num,
)

from photos.utils import (
    get_background_photo,
    get_project_photos,
    display_project_photo,
    upload_project_photo,
)

from overviews.views import edit_overview
from contractors.utils import get_state_full_name

from ratings.utils import (
    RATING_STAR_MAX,
    get_rating,
    get_user_rating_form,
)

from overviews.utils import (
    get_overview,
    get_overview_form,
)

from .models import Architect


# TODO: add a overview database
class ArchitectDetail(View):

    def __init__(self):
        self.model_name = 'architect'
        self.data_source = 'California Architects Board'
        self.score = None
        self.rank = None
        super(ArchitectDetail, self).__init__()

    def get_info_dict(self, request, o_id):
        model_name = self.model_name
        data_source = self.data_source
        score = self.score
        rank = self.rank
        architect = Architect.objects.get(lic_num=o_id)
        bgimage = get_background_photo(model_name=model_name, object_id=o_id)
        full_state_name = get_state_full_name(architect.state)
        lic_type = architect.lic_type.split('&')
        review = get_review(model_name=model_name, object_id=o_id, review_status='A')
        ratings = get_rating(model_name=model_name, object_id=o_id, review=review)
        p_lic_num = get_p_lic_num(request)
        project_photos = get_project_photos(model_name=model_name, object_id=o_id)
        review_form = get_review_form(request)
        user_rating_form = get_user_rating_form()
        overview = get_overview(
            model_name=model_name,
            object_id=o_id,
            instance=architect,
            data_source=data_source,
            score=score,
            rank=rank,
            full_state_name=full_state_name,
        )
        overview_form = get_overview_form(overview=overview)
        info_dict = {"architect": architect, "bg_image": bgimage, "overview": overview,
                     "score": score, "lic_type": lic_type, 'review': review,
                     "ratings": ratings, 'project_photos': project_photos, 'review_form': review_form,
                     "user_rating_form": user_rating_form, 'p_lic_num': p_lic_num, 'overview_form': overview_form}
        return info_dict

    def post(self, request, o_id):
        info_dict = self.get_info_dict(request, o_id)
        if request.POST.get('review'):
            return post_review(
                request=request,
                o_id=o_id,
                info_dict=info_dict,
                template_name='architect/architect.html',
            )
        elif request.POST.get('overview'):
            edit_overview(request, o_id)
            return redirect(request.path)
        else:
            raise Http404(_("Error Pages!"))

    def get(self, request, o_id):
        info_dict = self.get_info_dict(request, o_id)
        return render(request, 'architect/architect.html', {"info_dict": info_dict})


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
