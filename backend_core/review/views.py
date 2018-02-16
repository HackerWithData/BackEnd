# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseNotFound, Http404

from ratings.forms import get_user_rating_form
from ratings.utils import create_user_rating
from professionals.utils import check_professional_type
from .forms import get_review_form
from .utils import (
    create_review,
    create_review_photos,
    get_reviews,
)


def submit_review(request, professional):
    template_name = r'review/submit_review.html'
    if request.method == "POST":
        user_rating_form = get_user_rating_form(request.POST)
        review_form = get_review_form(request, method="POST")
        # TODO: assign a random password
        if review_form.is_valid() and user_rating_form.is_valid():
            review = create_review(
                request=request,
                professional=professional,
                review_form=review_form
            )
            create_user_rating(user_rating_form=user_rating_form, review=review)
            create_review_photos(request=request, review=review)
            return redirect(request.path)

    # other situation
    user_rating_form = get_user_rating_form()
    review_form = get_review_form(
        request=request,
        method="GET",
    )
    info_dict = {'review_form': review_form, "user_rating_form": user_rating_form, }
    return render(request, template_name, {"info_dict": info_dict})


def display_review(request, professional):
    if request.is_ajax() and request.method == "POST":
        template_name = r'review/display_review.html'
        review = get_reviews(model_name=model_name, object_id=o_id, review_status='A')
        info_dict = {"review": review}
        return render(request, template_name, {"info_dict": info_dict})
    else:
        raise Http404('No Pages Found.')
