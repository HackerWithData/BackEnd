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


class ProfessionalDetail(View):

    def __init__(self):
        self.model = None
        self.data_source = None
        self.score = None
        self.rank = None
        self.template_name = None
        self.info_dict = {}
        super(ProfessionalDetail, self).__init__()

    def get_professional_overview(self, request, o_id, instance):
        model_name = str(ContentType.objects.get_for_model(instance).name)
        full_state_name = get_state_full_name(instance.state)
        score = self.score
        rank = self.rank
        data_source = self.data_source
        overview = get_overview(
            model_name=model_name,
            object_id=o_id,
            **{
                'bus_name': instance.lic_name,
                'city': instance.city,
                'state': instance.state,
                'data_source': data_source,
                'score': score,
                'rank': rank,
                'full_state_name': full_state_name
            }
        )
        return overview

    def set_info_dict(self, request, o_id):
        score = self.score
        model = self.model
        model_name = str(ContentType.objects.get_for_model(model).name)
        instance = model.objects.get(lic_num=o_id)
        bgimage = get_background_photo(model_name=model_name, object_id=o_id)
        lic_type = instance.lic_type.split('&')
        review = get_review(model_name=model_name, object_id=o_id, review_status='A')
        ratings = get_rating(model_name=model_name, object_id=o_id, review=review)
        p_lic_num = get_p_lic_num(request)
        project_photos = get_project_photos(model_name=model_name, object_id=o_id)
        review_form = get_review_form(request)
        user_rating_form = get_user_rating_form()
        overview = self.get_professional_overview(request=request, o_id=o_id, instance=instance)
        overview_form = get_overview_form(overview=overview)
        info_dict = {
            model_name: instance,
            "bg_image": bgimage,
            "overview": overview,
            "score": score,
            "lic_type": lic_type,
            'review': review,
            "ratings": ratings,
            'project_photos': project_photos,
            'review_form': review_form,
            "user_rating_form": user_rating_form,
            'p_lic_num': p_lic_num,
            'overview_form': overview_form,
        }
        self.info_dict = info_dict

    def post(self, request, o_id):
        self.set_info_dict(request, o_id)
        info_dict = self.info_dict
        template_name = self.template_name
        if request.POST.get('review'):
            return post_review(
                request=request,
                o_id=o_id,
                info_dict=info_dict,
                template_name=template_name,
            )
        elif request.POST.get('overview'):
            edit_overview(request, o_id)
            return redirect(request.path)
        else:
            raise Http404(_("Error Pages!"))

    def get(self, request, o_id):
        self.set_info_dict(request, o_id)
        info_dict = self.info_dict
        template_name = self.template_name
        return render(request, template_name, {"info_dict": info_dict})
