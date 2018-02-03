# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _,  ugettext_lazy as _
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages

from review.utils import get_reviews, create_review
from review.forms import get_review_form
from review.views import submit_review as submit_review_, display_review as display_review_
from photos.utils import (
    get_bg_image,
    get_photos,
    upload_photo,
    display_project_photo,
    upload_project_photo,
)
from photos.views import background_photo_upload as backgroud_photo_upload_
from users.utils import get_p_id
from ratings.utils import (
    get_ratings,
    create_user_rating,
)
from ratings.forms import get_user_rating_form
from overviews.utils import get_overview
from overviews.forms import get_overview_form
from overviews.views import edit_overview
from projects.views import create_project
from .utils import (
    get_professional_instance,
    get_professional,
    get_professional_info as get_pro_info,
)
from .utils import get_state_full_name
from .models import Professional


class ProfessionalDetail(View):
    fields = ()
    template_name = None
    info_dict = dict()
    data_source = None
    model_name = None

    def get_professional_bg_image(self, **kwargs):
        return get_bg_image(model_name=kwargs.get('model_name'), object_id=kwargs.get('o_id'))

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

    def get_professional_p_id(self, **kwargs):
        return get_p_id(kwargs.get('request'))

    def get_professional_project_photos(self, **kwargs):
        return get_photos(model_name=kwargs.get('model_name'), object_id=kwargs.get('o_id'))

    def get_professional_review_form(self, **kwargs):
        return get_review_form(request=kwargs.get('request'), method='GET')

    def get_professional_user_rating_form(self, **kwargs):
        return get_user_rating_form()

    def get_professional_score(self, **kwargs):
        return None

    def get_professional_rank(self, **kwargs):
        return None

    def set_info_dict(self, request, o_id):
        model_name = self.model_name
        instance = get_professional_instance(model_type=model_name, lic_num=o_id)
        if instance is None:
            raise Http404(_("Error Pages!"))
        model = instance.__class__
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
    #TODO: need to change here with below views
    def get_professional_overview(self, **kwargs):
        return get_overview(
            model_name=kwargs.get('model_name'),
            object_id=kwargs.get('o_id'),
            message=self.get_overview_message(**kwargs)
        )

    def get_professional_overview_form(self, **kwargs):
        return get_overview_form(data=kwargs.get('overview', None))
    def get_overview_message(self, **kwargs):
        return ""

    def post(self, request, o_id):
        self.set_info_dict(request, o_id)
        info_dict = self.info_dict
        template_name = self.template_name
        if request.POST.get('review', None):
            user_rating_form = get_user_rating_form(request.POST)
            review_form = get_review_form(request, method="POST")
            if review_form.is_valid() and user_rating_form.is_valid():
                try:
                    review = create_review(
                        request=request,
                        o_id=o_id,
                        review_form=review_form,
                    )
                except ValueError:
                    review = create_review(
                        request=request,
                        o_id=info_dict.get(self.model_name).id,
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

#TODO: check every source is correctly referenced
#TODO: add missing source
#TODO: correct the wrong reference source.
class ProfessionalView(ProfessionalDetail):
    #TODO: this would be change later
    data_source = 'California Architects Board'
    template_name = 'professional/professional.html'
    model_name = 'professional'

    fields = (
        'bg_image',
        'review',
        'ratings',
        'project_photos',
        'review_form',
        'p_id',
        'user_rating_form',
        'overview',
        'overview_form',
    )

    def get_professional_info(self, **kwargs):
        return get_pro_info(professional=kwargs.get('instance'))

    def set_info_dict(self, request, uuid):
        model_name = self.model_name
        instance = get_professional(uuid=uuid)
        if instance is None:
            raise Http404(_("Error Pages!"))
        model = instance.__class__
        kwargs = {
            'request': request,
            'o_id': instance.id,
            'model': model,
            'model_name': model_name,
            'instance': instance,
        }
        self.info_dict.update({model_name: instance})
        for field in self.fields:
            exec('field_val = self.get_professional_{field}(**kwargs)'.format(field=field))
            kwargs.update({field: field_val})
            self.info_dict.update({field: field_val})

    def get_professional_overview(self, **kwargs):
        message = _(
            """{lic_name} is located in {csp}. According to real-time dat.a analysis, this licensed contractor's hoome score 
                    is {score} and is rated as {rank}. The License is verified as active when we checked last time. If you would
                     like to know {lic_name} more, please contact us and we will share more information and data about this
                      contractor to you."""
        ).format(
            type=kwargs.get('type'),
            lic_name=kwargs.get('instance').name,
            csp=kwargs.get('instance').csp,
            data_source=self.data_source,
            score=kwargs.get('score'),
            rank=kwargs.get('letter_grade'),
            full_state_name=kwargs.get('full_state_name'),
        )
        return message


def _get_professional_id_by_uuid(uuid):
    professional = get_professional(uuid=uuid)
    if not professional:
        raise Http404(_("Error Pages!"))
    o_id = professional.id
    return o_id


def display_project_photos(request, uuid):
    template_name = 'contractor/contractor_project_photo.html'
    o_id = _get_professional_id_by_uuid(uuid)
    return display_project_photo(
        request=request,
        o_id=o_id,
        model=Professional,
        template_name=template_name,
    )


def upload_project_photos(request, uuid):
    o_id = _get_professional_id_by_uuid(uuid)
    success_url = reverse('professional', args=[uuid])
    model_name = 'professional'
    template_name = 'contractor/contractor_project_photos_upload.html'
    return upload_project_photo(
        request=request,
        o_id=o_id,
        success_url=success_url,
        model_name=model_name,
        template_name=template_name,
    )


def display_review(request, uuid):
    o_id = _get_professional_id_by_uuid(uuid)
    return display_review_(request=request, o_id=o_id)


def submit_review(request, uuid):
    o_id = _get_professional_id_by_uuid(uuid)
    return submit_review_(request=request, o_id=o_id)


def background_photo_upload(request, uuid):
    o_id = _get_professional_id_by_uuid(uuid)
    success_url = reverse('professional', args=[uuid])
    return backgroud_photo_upload_(request=request, o_id=o_id, success_url=success_url)


def professional_create_project(request, uuid):
    o_id = _get_professional_id_by_uuid(uuid)
    return create_project(request, professional_type='professional', lic_id=o_id)