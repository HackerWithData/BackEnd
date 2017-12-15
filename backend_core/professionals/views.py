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
)
from photos.utils import (
    get_bgimage,
    get_project_photos,
    display_project_photo,
    upload_project_photo,
)
from overviews.views import edit_overview
from contractors.utils import get_state_full_name
from users.utils import get_p_lic_num
from ratings.utils import (
    RATING_STAR_MAX,
    get_ratings,
    get_user_rating_form,
)
from overviews.utils import (
    get_overview,
    get_overview_form,
)


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
        return get_review(
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
        return get_project_photos(model_name=kwargs.get('model_name'), object_id=kwargs.get('o_id'))

    def get_professional_review_form(self, **kwargs):
        return get_review_form(request=kwargs.get('request'))

    def get_professional_user_rating_form(self, **kwargs):
        return get_user_rating_form()

    def get_professional_overview(self, **kwargs):
        return get_overview(
            model_name=kwargs.get('model_name'),
            object_id=kwargs.get('o_id'),
            message=self.get_overview_message(**kwargs)
        )

    def get_professional_overview_form(self, **kwargs):
        return get_overview_form(overview=kwargs.get('overview', None))

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

