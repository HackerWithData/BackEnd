# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from forms import ReviewForm
from ratings.forms import UserRatingForm
from contractors.models import Contractor
from disk.models import UserFile, ProjectImage
from ratings.models import UserRating
from models import Review
import datetime
# Create your views here.

def submit_review(request,contractor_id):
    #form_class = ReviewForm
    template_name = 'contractor/contractor_review.html'
    rate_star_max_length = 10
    rate_star_list = [str(i) for i in range(rate_star_max_length, 0, -1)]
    contractor = Contractor.objects.get(LicNum=contractor_id)
    bgimage = UserFile.objects.get(userName=contractor.BusName).uploadFile

    if request.method == "POST":

        user_rating_form = UserRatingForm(request.POST)
        #sign_up_form = SignUpForm2(request.POST)
        review_form = ReviewForm(request.POST)
        if review_form.is_valid() and user_rating_form.is_valid():
            user = User(email=review_form.cleaned_data['email'],
                        username='asdTalk5',
                        last_name=review_form.cleaned_data['last_name'],
                        first_name=review_form.cleaned_data['first_name'])

            #username=review_form['username'],

            print(review_form['project_date'])
            review = Review(contractor=contractor,
                            user=user,
                            comments=review_form.cleaned_data['comments'],
                            project_date=review_form.cleaned_data['project_date'],
                            project_zipcode=review_form.cleaned_data['project_zipcode'],
                            project_cost=review_form.cleaned_data['project_cost'],
                            project_duration=review_form.cleaned_data['project_duration'],
                            project_address=review_form.cleaned_data['project_address'],
                            is_anonymous=review_form.cleaned_data['is_anonymous'])
            user.save()
            review.save()
            for item in user_rating_form:
                print item, item.label
                user_rating = UserRating(review=review,
                                         rating_type=item.label,
                                         rating_score=item.cleaned_data)
                user_rating.save()
            return render(request, 'disk/uploadsuccess.html')  # redirect('/')#

    #other situation
    user_rating_form = UserRatingForm()
    if request.user.is_authenticated:
        review_form = ReviewForm(initial={'first_name': request.user.first_name,
                                          'last_name': request.user.last_name,
                                          'contractor': Contractor.objects.get(pk=contractor_id),
                                          'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
    else:
        review_form = ReviewForm(initial={'contractor': Contractor.objects.get(pk=contractor_id),
                                          'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})

    info_dict = {'review_form': review_form, "user_rating_form": user_rating_form, "rate_star_list": rate_star_list, "contractor": contractor,
                 "bgimage": bgimage}
    return render(request, template_name, {"info_dict": info_dict})


