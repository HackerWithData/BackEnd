# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
    # ugettext_lazy as _
from django.views import View

from photos.forms import PhotoForm
from photos.models import Photo, BackgroundPhoto
from ratings.forms import UserRatingForm
from ratings.models import UserRating, Rating
from review.forms import ReviewForm
from review.models import Review
from overviews.forms import OverviewForm
from overviews.models import Overview
from overviews.views import edit_overview
from contractors.utils import convert_hscore_to_rank, get_state_full_name, avg_rating
from professionals.utils import check_professional_type

from .models import Meister
# from contractors.views import submit_review
# Create your views here.


class MeisterDetail(View):

    def get(self, request, o_id):
        meister = Meister.objects.get(lic_num=o_id)
        try:
            bgimage = BackgroundPhoto.objects.get(content_type=ContentType.objects.get(model='meister'),
                                                  object_id=o_id)
        except BackgroundPhoto.DoesNotExist:
            bgimage = None
        #data_source = 'California Contractors State License Board'

        try:
            review = Review.objects.filter(content_type=ContentType.objects.get(model='meister'),
                                           object_id=o_id, review_status='A')
        except:
            review = None
        # rating
        RATING_STAR_MAX = 10
        meister_ratings = Rating.objects.filter(content_type=ContentType.objects.get(model='meister'),
                                                   object_id=o_id).order_by('ratings_average')
        ratings = {}
        ratings['stars'] = range(RATING_STAR_MAX, 0, -1)
        # TODO:NEED TO CHANGE HERE
        ratings['overall'] = (avg_rating(review, 'Q') + avg_rating(review, 'E') + avg_rating(review, 'L')) / 3
        try:
            ratings['rate'] = [(item.average, round(item.average * 1.0 / RATING_STAR_MAX, 2)) for item in
                               meister_ratings]
        except:
            pass
        project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='meister'),
                                              object_id=o_id)
        if request.user.is_anonymous():
            p_lic_num = None
        else:
            try:
                p_lic_num = str(request.user.professional_profiles.first().professional.lic_num)
            except:
                p_lic_num = -1

        # other situation
        user_rating_form = UserRatingForm()
        if request.user.is_authenticated:
            review_form = ReviewForm(initial={'first_name': request.user.first_name,
                                              'last_name': request.user.last_name,
                                              'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
        else:
            review_form = ReviewForm(initial={
                'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
        try:
            overview = Overview.objects.get(content_type=ContentType.objects.get(model='meister'),
                                            object_id=o_id).overview
        except Overview.DoesNotExist:
            overview = _("""{lic_name} is a professional located in {full_state_name}. The professional is verified as 
            active when we checked last time. If you would like to know {lic_name} more, please contact us and we will 
            share more information and data about this meister to you.""").format(lic_name=meister.lic_name,
            full_state_name=get_state_full_name(meister.state))
        overview_form = OverviewForm(initial={'overview': overview})
        info_dict = {"meister": meister, "bg_image": bgimage, "overview": overview, 'review': review,
                     "ratings": ratings, 'project_photos': project_photos, 'review_form': review_form,
                     "user_rating_form": user_rating_form, 'p_lic_num': p_lic_num, 'overview_form': overview_form}
        template_name = 'meister/meister.html'
        return render(request, template_name, {"info_dict": info_dict})

    def post(self, request, o_id):
        template_name = 'meister/meister.html'
        meister = Meister.objects.get(lic_num=o_id)
        try:
            bgimage = BackgroundPhoto.objects.get(content_type=ContentType.objects.get(model='meister'),
                                                  object_id=o_id)
        except BackgroundPhoto.DoesNotExist:
            bgimage = None
        #data_source = 'California Contractors State License Board'

        try:
            review = Review.objects.filter(content_type=ContentType.objects.get(model='meister'),
                                           object_id=o_id, review_status='A')
        except:
            review = None
        # rating
        RATING_STAR_MAX = 10
        meister_ratings = Rating.objects.filter(content_type=ContentType.objects.get(model='meister'),
                                                   object_id=o_id).order_by('ratings_average')
        ratings = {}
        ratings['stars'] = range(RATING_STAR_MAX, 0, -1)
        # TODO:NEED TO CHANGE HERE
        ratings['overall'] = (avg_rating(review, 'Q') + avg_rating(review, 'E') + avg_rating(review, 'L')) / 3
        try:
            ratings['rate'] = [(item.average, round(item.average * 1.0 / RATING_STAR_MAX, 2)) for item in
                               meister_ratings]
        except:
            pass
        project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='meister'),
                                              object_id=o_id)
        if request.user.is_anonymous():
            p_lic_num = None
        else:
            try:
                p_lic_num = str(request.user.professional_profiles.first().professional.lic_num)
            except:
                p_lic_num = -1

        # other situation
        user_rating_form = UserRatingForm()
        if request.user.is_authenticated:
            review_form = ReviewForm(initial={'first_name': request.user.first_name,
                                              'last_name': request.user.last_name,
                                              'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
        else:
            review_form = ReviewForm(initial={
                'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
        try:
            overview = Overview.objects.get(content_type=ContentType.objects.get(model='meister'),
                                            object_id=o_id).overview
        except Overview.DoesNotExist:
            overview = _("""{lic_name} is a professional located in {full_state_name}. The professional is verified as 
            active when we checked last time. If you would like to know {lic_name} more, please contact us and we will 
            share more information and data about this meister to you.""").format(lic_name=meister.lic_name,
            full_state_name=get_state_full_name(meister.state))
        overview_form = OverviewForm(initial={'overview': overview})
        info_dict = {"meister": meister, "bg_image": bgimage, "overview": overview, 'review': review,
                     "ratings": ratings, 'project_photos': project_photos, 'review_form': review_form,
                     "user_rating_form": user_rating_form, 'p_lic_num': p_lic_num, 'overview_form': overview_form}

        if request.POST.get('review'):
            user_rating_form = UserRatingForm(request.POST)
            review_form = ReviewForm(request.POST)
            # TODO: assign a random password
            # TODO: validator doesn't work
            if review_form.is_valid() and user_rating_form.is_valid():
                model_type = check_professional_type(request)
                review = review_form.save( commit=False)
                if request.user.is_authenticated():
                    review.user = request.user
                review.content_type = ContentType.objects.get(model=model_type)
                review.object_id = o_id
                review.save()

                for field in user_rating_form.cleaned_data:
                    user_rating = UserRating(review=review,
                                             rating_type=field[0].upper(),
                                             rating_score=int(user_rating_form.cleaned_data[field]))
                    user_rating.save()
                # direct to the page to upload photos
                # TODO: ADD PHOTOFORM VALIDATION FOR SECURITY
                content_type = ContentType.objects.get(model='review')
                object_id = int(review.id)
                files = request.FILES.getlist('project photos')
                if len(files) > 0:
                    for f in files:
                        instance = Photo.objects.create(img=f, title=f.name, content_type=content_type,
                                                        object_id=object_id)
                        instance.save()
                else:
                    pass
                # request.session.pop('review_form', None)
                # TODO: redirect the sucess url and add bootstrap messages: success
                return redirect(request.path)
            else:
                # request.session.update({'review_form': review_form.data})
                info_dict['review_form'] = review_form
                info_dict["user_rating_form"] = user_rating_form
                messages.warning(request, _('Submit Failed. Please verify your content is correct.'))
                return render(request, template_name, {"info_dict": info_dict})
        elif request.POST.get('overview'):
            edit_overview(request, o_id)
            return redirect(request.path)
        else:
            raise Http404(_("Error Pages!"))


#TODO: this function is derecated. Jeremy will revise this part and make it reuseable.
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


# TODO: simplify this function into one (contractor, architect, designer)
def display_project_photos(request, o_id):
    if request.is_ajax() and request.method == "POST":
        template_name = 'meister/meister_project_photo.html'
        project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='meister'),
                                              object_id=o_id)
        info_dict = {'project_photos': project_photos}  # , 'contractor': contractor
        return render(request, template_name, {'info_dict': info_dict})
    else:
        raise Http404(_('No Pages Found.'))


def upload_project_photos(request, o_id):
    if request.user.is_anonymous():
        p_lic_num = None
    else:
        try:
            p_lic_num = str(request.user.professional_profiles.first().professional.lic_num)
        except:
            p_lic_num = None
    if str(p_lic_num) == str(o_id):
        template_name = 'meister/meister_project_photos_upload.html'  # Replace with your template.
        success_url = '/meister/' + o_id  # Replace with your URL or reverse().

        if request.method == "POST":
            form = PhotoForm(request.POST, request.FILES)
            content_type = ContentType.objects.get(model='meister')
            object_id = int(o_id)
            files = request.FILES.getlist('img')
            if form.is_valid():
                if len(files) > 0:
                    for f in files:
                        instance = Photo.objects.create(img=f, title=f.name, content_type=content_type,
                                                        object_id=object_id)
                        instance.save()
                else:
                    pass
                return redirect(success_url)
        form = PhotoForm()
        info_dict = {'form': form}
        return render(request, template_name, info_dict)
    else:
        raise Http404(_('No Pages Found.'))
