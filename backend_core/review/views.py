# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.shortcuts import render, redirect
from users.models import User
from forms import ReviewForm
from ratings.forms import UserRatingForm
from ratings.models import UserRating
from models import Review
from django.contrib.auth.hashers import make_password
from contractors.models import Contractor
from django.contrib.contenttypes.models import ContentType
from photos.models import Photo
import datetime
from users.utils import CONSUMER
from django.conf import settings
from professionals.utils import check_professional_type
from django.http import HttpResponseNotFound, Http404
# Create your views here.


def submit_review(request, o_id):
    template_name = r'review/submit_review.html'
    if request.method == "POST":

        user_rating_form = UserRatingForm(request.POST)
        # sign_up_form = SignUpForm2(request.POST)
        review_form = ReviewForm(request.POST)
        # TODO: assign a random password
        if review_form.is_valid() and user_rating_form.is_valid():
            # User = #ContentType.objects.get_for_model(settings.AUTH_USER_MODEL)
            #TODO: anyone could leave message and add recaptcha.
            user = User(email=review_form.cleaned_data['email'],
                        username=review_form.cleaned_data['email'],
                        last_name=review_form.cleaned_data['last_name'],
                        first_name=review_form.cleaned_data['first_name'],
                        password=make_password("aaaaaaa"))
            user.save()
            model_type = check_professional_type(request)
            review = Review(content_type=ContentType.objects.get(model=model_type),
                            object_id=o_id,
                            user=user,
                            comments=review_form.cleaned_data['comments'],
                            project_date=review_form.cleaned_data['project_date'],
                            project_zipcode=review_form.cleaned_data['project_zipcode'],
                            project_cost=review_form.cleaned_data['project_cost'],
                            project_duration=review_form.cleaned_data['project_duration'],
                            project_address=review_form.cleaned_data['project_address'],
                            is_anonymous=review_form.cleaned_data['is_anonymous'],
                            project_type=review_form.cleaned_data['project_type'])
            review.save()
            for field in user_rating_form.cleaned_data:
                user_rating = UserRating(review=review,
                                         rating_type=field[0].upper(),
                                         rating_score=int(user_rating_form.cleaned_data[field]))
                user_rating.save()
            # direct to the page to upload photos
            content_type = ContentType.objects.get(model='review')
            object_id = int(review.id)
            files = request.FILES.getlist('project photos')
            if len(files) > 0:
                for f in files:
                    instance = Photo.objects.create(img=f, title=f.name, content_type=content_type, object_id=object_id)
                    instance.save()
            else:
                pass
            return redirect(request.path)

    # other situation
    user_rating_form = UserRatingForm()
    if request.user.is_authenticated:
        review_form = ReviewForm(initial={'first_name': request.user.first_name,
                                          'last_name': request.user.last_name,
                                          'contractor': Contractor.objects.get(pk=o_id),
                                          'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
    else:
        review_form = ReviewForm(initial={'contractor': Contractor.objects.get(pk=o_id),
                                          'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})

    info_dict = {'review_form': review_form, "user_rating_form": user_rating_form, }
    return render(request, template_name, {"info_dict": info_dict})


def display_review(request, o_id):
    if request.is_ajax() and request.method == "POST":
        template_name = r'review/display_review.html'
        model_type = check_professional_type(request)
        review = Review.objects.filter(content_type=ContentType.objects.get(model=model_type), object_id=o_id,
                                       review_status='A')
        # other situation
        info_dict = {"review": review}
        return render(request, template_name, {"info_dict": info_dict})
    else:
        raise Http404('No Pages Found.')
