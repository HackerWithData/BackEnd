# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.utils.translation import ugettext as _,  ugettext_lazy as _
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.contenttypes.models import ContentType

from review.utils import get_reviews, create_review
from review.forms import get_review_form
from photos.utils import (
    get_bgimage,
    get_photo,
    display_project_photo,
    upload_project_photo,
    upload_photo,
)
from overviews.views import edit_overview
from contractors.utils import get_state_full_name
from users.utils import get_p_lic_num
from ratings.utils import (
    get_ratings,
    create_user_rating,
)
from ratings.models import RATING_STAR_MAX
from ratings.forms import get_user_rating_form
from overviews.utils import get_overview
from overviews.forms import get_overview_form


class ProfessionalDetail(View):
    fields = ()
    template_name = None
    info_dict = dict()
    data_source = None
    model = None

    def get_professional_bgimage(self, **kwargs):
        return get_bgimage(model_name=kwargs.get('model_name'), object_id=kwargs.get('o_id'))

    def get_professional_lic_type(self, **kwargs):
        return kwargs.get('instance').lic_type.split('&')

    def get_professional_review(self, **kwargs):
        return get_reviews(
            model_name=kwargs.get('model_name'),
            object_id=kwargs.get('o_id'),
            review_status=kwargs.get('review_status', 'A'),
        )

    def get_professional_full_state_name(self, **kwargs):
        return get_state_full_name(kwargs.get('instance').state)

    def get_professional_ratings(self, **kwargs):
        return get_ratings(
            model_name=kwargs.get('model_name'),
            object_id=kwargs.get('o_id'),
            review=kwargs.get('review', None),
        )

    def get_professional_p_lic_num(self, **kwargs):
        return get_p_lic_num(kwargs.get('request'))

    def get_professional_project_photos(self, **kwargs):
        return get_photo(model_name=kwargs.get('model_name'), object_id=kwargs.get('o_id'))

    def get_professional_review_form(self, **kwargs):
        return get_review_form(request=kwargs.get('request'), method='GET')

    def get_professional_user_rating_form(self, **kwargs):
        return get_user_rating_form()

    def get_professional_overview(self, **kwargs):
        return get_overview(
            model_name=kwargs.get('model_name'),
            object_id=kwargs.get('o_id'),
            message=self.get_overview_message(**kwargs)
        )

    def get_professional_overview_form(self, **kwargs):
        return get_overview_form(data=kwargs.get('overview', None))

    def get_professional_score(self, **kwargs):
        return None

    def get_professional_rank(self, **kwargs):
        return None

    def get_overview_message(self, **kwargs):
        return ""

    def set_info_dict(self, request, o_id):
        model = self.model
        model_name = str(ContentType.objects.get_for_model(model).name)
        instance = model.objects.get(lic_num=o_id)
        kwargs = {
            'request': request,
            'o_id': o_id,
            'model': model,
            'model_name': model_name,
            'instance': instance,
        }
        self.info_dict.update({model_name: instance})
        for field in self.fields:
            exec('field_val = self.get_professional_{field}(**kwargs)'.format(field=field))
            kwargs.update({field: field_val})
            self.info_dict.update({field: field_val})

    def post(self, request, o_id):
        self.set_info_dict(request, o_id)
        info_dict = self.info_dict
        template_name = self.template_name
        if request.POST.get('review', None):
            user_rating_form = get_user_rating_form(request.POST)
            review_form = get_review_form(request, method="POST")
            if review_form.is_valid() and user_rating_form.is_valid():
                review = create_review(
                    request=request,
                    o_id=o_id,
                    review_form=review_form,
                )
                create_user_rating(user_rating_form=user_rating_form, review=review)
                upload_photo(request=request, model_name='review', o_id=review.id)
                return redirect(request.path)
            else:
                info_dict['review_form'] = review_form
                info_dict["user_rating_form"] = user_rating_form
                messages.warning(request, _('Submit Failed. Please verify your content is correct.'))
                return render(request, template_name, {"info_dict": info_dict})
        elif request.POST.get('overview', None):
            edit_overview(request, o_id)
            return redirect(request.path)
        else:
            raise Http404(_("Error Pages!"))

    def get(self, request, o_id):
        self.set_info_dict(request, o_id)
        info_dict = self.info_dict
        template_name = self.template_name
        return render(request, template_name, {"info_dict": info_dict})

