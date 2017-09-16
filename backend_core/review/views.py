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
from photos.models import Photo
from ratings.models import UserRating
from models import Review
import datetime
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseNotFound
# Create your views here.


def submit_review(request, contractor_id):
    template_name = r'review/submit_review_contractor.html'

    contractor = Contractor.objects.get(LicNum=contractor_id)
    try:
        bgimage = UserFile.objects.get(userName=contractor.BusName).uploadFile
    except:
        bgimage = None

    if request.method == "POST":

        user_rating_form = UserRatingForm(request.POST)
        #sign_up_form = SignUpForm2(request.POST)
        review_form = ReviewForm(request.POST)
        #TODO: assign a random password
        if review_form.is_valid() and user_rating_form.is_valid():
            user = User(email=review_form.cleaned_data['email'],
                        username=review_form.cleaned_data['email'],
                        last_name=review_form.cleaned_data['last_name'],
                        first_name=review_form.cleaned_data['first_name'],
                        password="aaaaaaa")
            #username=review_form['username'],
            user.save()
            #print(review_form['project_date'])
            review = Review(contractor=contractor,
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
            #direct to the page to upload photos
            content_type = ContentType.objects.get(model='review')
            object_id = int(review.id)
            files = request.FILES.getlist('project photos')
            if len(files) > 0:
                for f in files:
                    instance = Photo.objects.create(img=f, title=f.name, content_type=content_type,object_id=object_id)
                    instance.save()
            else:
                pass
            return render(request, 'disk/uploadsuccess.html' )

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

    info_dict = {'review_form': review_form, "user_rating_form": user_rating_form, "contractor": contractor,
                 "bgimage": bgimage}
    return render(request, template_name, {"info_dict": info_dict})


def display_review(request, contractor_id):
    if request.is_ajax() and request.method == "POST":
        template_name = r'contractor/contractor_review.html'

        contractor = Contractor.objects.get(LicNum=contractor_id)
        try:
            bgimage = UserFile.objects.get(userName=contractor.BusName).uploadFile
        except:
            bgimage = None

        review = Review.objects.filter(contractor=contractor, review_status='A')

        #other situation
        info_dict = {"contractor": contractor, "bgimage": bgimage, "review": review}
        return render(request, template_name, {"info_dict": info_dict})
    else:
        return HttpResponseNotFound('No Pages Found.')



