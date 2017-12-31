# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseNotFound, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _, ugettext_lazy as _
from django.views import View
from hscore.models import Hscore
from photos.forms import PhotoForm
from photos.models import Photo, BackgroundPhoto
from ratings.forms import UserRatingForm
from ratings.models import UserRating, Rating
from review.forms import ReviewForm
from review.models import Review
from users.models import User
from overviews.forms import OverviewForm
from overviews.models import Overview
from overviews.views import edit_overview
from models import Contractor, BondHistory, WorkerCompensationHistory, ComplaintOverall
from utils import convert_hscore_to_rank, get_state_full_name, avg_rating
from professionals.utils import check_professional_type


# Create your views here.
class Complaint1:
    def __init__(self):
        self.case = 0
        self.citation = 0
        self.arbitration = 0
        self.complaint = 0


# def submit_review(request, o_id):
#     user_rating_form = UserRatingForm(request.POST)
#     review_form = ReviewForm(request.POST)
#     # TODO: assign a random password
#     # TODO: validator doesn't work
#     if review_form.is_valid() and user_rating_form.is_valid():
#         # User = #ContentType.objects.get_for_model(settings.AUTH_USER_MODEL)
#         user = User(email=review_form.cleaned_data['email'],
#                     username=review_form.cleaned_data['email'],
#                     last_name=review_form.cleaned_data['last_name'],
#                     first_name=review_form.cleaned_data['first_name'],
#                     password=make_password("aaaaaaa"))
#         user.save()
#         model_type = check_professional_type(request)
#         review = Review(content_type=ContentType.objects.get(model=model_type),
#                         object_id=o_id,
#                         user=user,
#                         comments=review_form.cleaned_data['comments'],
#                         project_date=review_form.cleaned_data['project_date'],
#                         project_zipcode=review_form.cleaned_data['project_zipcode'],
#                         project_cost=review_form.cleaned_data['project_cost'],
#                         project_duration=review_form.cleaned_data['project_duration'],
#                         project_address=review_form.cleaned_data['project_address'],
#                         is_anonymous=review_form.cleaned_data['is_anonymous'],
#                         project_type=review_form.cleaned_data['project_type'])
#         review.save()
#         for field in user_rating_form.cleaned_data:
#             user_rating = UserRating(review=review,
#                                      rating_type=field[0].upper(),
#                                      rating_score=int(user_rating_form.cleaned_data[field]))
#             user_rating.save()
#         # direct to the page to upload photos
#         # TODO: ADD PHOTOFORM VALIDATION FOR SECURITY
#         content_type = ContentType.objects.get(model='review')
#         object_id = int(review.id)
#         files = request.FILES.getlist('project photos')
#         if len(files) > 0:
#             for f in files:
#                 instance = Photo.objects.create(img=f, title=f.name, content_type=content_type, object_id=object_id)
#                 instance.save()
#         else:
#             pass
#         # request.session.pop('review_form', None)
#         # TODO: redirect the sucess url and add bootstrap messages: success
#         return redirect(request.path)
#     else:
#         # request.session.update({'review_form': review_form.data})
#         info_dict = {'review_form': review_form, "user_rating_form": user_rating_form}
#         return render(request, 'contractor/contractor.html', {"info_dict": info_dict})


class ContractorDetail(View):
    def get(self, request, contractor_id):
        # contractor info
        contractor = Contractor.objects.get(lic_num=contractor_id)
        # contractor background image
        o_id = contractor.lic_id
        try:
            bgimage = BackgroundPhoto.objects.get(content_type=ContentType.objects.get(model='contractor'),
                                                  object_id=o_id)
        except:
            bgimage = None

        bh = BondHistory.objects.filter(contractor_id=o_id).order_by('-bond_effective_date').first()
        wh = WorkerCompensationHistory.objects.filter(contractor_id=o_id).order_by(
            '-insur_effective_date').first()

        data_source = 'California Contractors State License Board'
        try:
            if contractor_id.startswith('TX'):
                hscore = Hscore.objects.create(contractor=contractor, score=None, rank=None, max=None)
            else:
                hscore = Hscore.objects.get(contractor_id=o_id)
        except:
            hscore = Hscore.objects.create(contractor=contractor, score=None, rank=None, max=None)

        letter_grade = convert_hscore_to_rank(hscore)
        full_state_name = get_state_full_name(contractor.state)
        # Lic Type
        lic_type = contractor.lic_type.split('&')
        # review
        try:

            review = Review.objects.filter(content_type=ContentType.objects.get(model='contractor'),
                                               object_id=o_id, review_status='A')
        except:
            review = None
        # rating

        RATING_STAR_MAX = 10
        ratings = {}
        ratings['stars'] = range(RATING_STAR_MAX, 0, -1)
        if contractor_id.startswith('TX'):
            ratings['overall'] = 0
            ratings['rate'] = 0

        else:
            contractor_ratings = Rating.objects.filter(content_type=ContentType.objects.get(model='contractor'),
                                                       object_id=o_id).order_by('ratings_average')

            # TODO:NEED TO CHANGE HERE
            ratings['overall'] = (avg_rating(review, 'Q') + avg_rating(review, 'E') + avg_rating(review, 'L')) / 3
            try:
                ratings['rate'] = [(item.average, round(item.average * 1.0 / RATING_STAR_MAX, 2)) for item in
                                   contractor_ratings]
            except:
                pass
        try:
            project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='contractor'),
                                                  object_id=o_id)
        except:
            project_photos = None
        try:
            if (contractor.lic_expire_date is not None) and (contractor.lic_expire_date < datetime.date.today()):
                length = int(contractor.lic_expire_date.year - contractor.lic_issue_date.year)
            elif (not contractor.lic_expire_date) and (not contractor.lic_issue_date):
                length = 0
            else:
                length = int(datetime.date.today().year - contractor.lic_issue_date.year)
        except:
            length = "N/A"
        # test issue, won't happen in prod


        try:
            complaint = ComplaintOverall.objects.get(contractor=contractor)
        except:
            complaint = Complaint1
            complaint.case = 0
            complaint.citation = 0
            complaint.arbitration = 0
            complaint.complaint = 0

        if request.user.is_anonymous():
            p_lic_num = None
        else:
            try:
                p_lic_num = str(request.user.professional_profiles.first().professional.lic_num)
            except:
                p_lic_num = None

        # other situation
        user_rating_form = UserRatingForm()
        # review_form = request.session.get('review_form', None)
        # if review_form is None:
        if request.user.is_authenticated:
            review_form = ReviewForm(initial={'first_name': request.user.first_name,
                                              'last_name': request.user.last_name,
                                              'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
        else:
            review_form = ReviewForm(initial={
                'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})

        try:
            overview = Overview.objects.get(content_type=ContentType.objects.get(model='contractor'),
                                            object_id=o_id).overview
        except:
            overview = _("""{lic_name} is a contractor company located in {csp} . The company holds a license number 
            according to {data_source}. According to real-time data analysis, this licensed contractor's hoome score 
            is {score} and is rated as {rank}. The License is verified as active when we checked last time. If you would
             like to know {lic_name} more, please contact us and we will share more information and data about this
              contractor to you.""").format(lic_name=contractor.lic_name, csp=contractor.csp, data_source=data_source,
                                            score=hscore.score, rank=letter_grade, full_state_name=full_state_name)

        overview_form = OverviewForm(initial={'overview': overview})

        info_dict = {"contractor": contractor, "bg_image": bgimage, "overview": overview, 'review': review,
                     "score": hscore.score, 'bond_history': bh, "wc_history": wh, "lic_type": lic_type,
                     "ratings": ratings, 'project_photos': project_photos, 'review_form': review_form,
                     "user_rating_form": user_rating_form, "complaint": complaint, "length": length,
                     'p_lic_num': p_lic_num, 'rank': letter_grade, 'overview_form': overview_form}

        return render(request, 'contractor/contractor.html', {"info_dict": info_dict})

    def post(self, request, contractor_id):
        # contractor info
        contractor = Contractor.objects.get(lic_num=contractor_id)
        # contractor background image
        o_id = contractor.lic_id
        try:
            bgimage = BackgroundPhoto.objects.get(content_type=ContentType.objects.get(model='contractor'),
                                                  object_id=o_id)
        except:
            bgimage = None

        bh = BondHistory.objects.filter(contractor_id=o_id).order_by('-bond_effective_date').first()
        wh = WorkerCompensationHistory.objects.filter(contractor_id=o_id).order_by(
            '-insur_effective_date').first()

        data_source = 'California Contractors State License Board'
        try:
            if contractor_id.startswith('TX'):
                hscore = Hscore.objects.create(contractor=contractor, score=None, rank=None, max=None)
            else:
                hscore = Hscore.objects.get(contractor_id=o_id)
        except:
            hscore = Hscore.objects.create(contractor=contractor, score=None, rank=None, max=None)

        letter_grade = convert_hscore_to_rank(hscore)
        full_state_name = get_state_full_name(contractor.state)
        # Lic Type
        lic_type = contractor.lic_type.split('&')
        # review
        try:

            review = Review.objects.filter(content_type=ContentType.objects.get(model='contractor'),
                                               object_id=o_id, review_status='A')
        except:
            review = None
        # rating

        RATING_STAR_MAX = 10
        ratings = {}
        ratings['stars'] = range(RATING_STAR_MAX, 0, -1)
        if contractor_id.startswith('TX'):
            ratings['overall'] = 0
            ratings['rate'] = 0

        else:
            contractor_ratings = Rating.objects.filter(content_type=ContentType.objects.get(model='contractor'),
                                                       object_id=o_id).order_by('ratings_average')

            # TODO:NEED TO CHANGE HERE
            ratings['overall'] = (avg_rating(review, 'Q') + avg_rating(review, 'E') + avg_rating(review, 'L')) / 3
            try:
                ratings['rate'] = [(item.average, round(item.average * 1.0 / RATING_STAR_MAX, 2)) for item in
                                   contractor_ratings]
            except:
                pass
        try:
            project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='contractor'),
                                                  object_id=o_id)
        except:
            project_photos = None
        try:
            if (contractor.lic_expire_date is not None) and (contractor.lic_expire_date < datetime.date.today()):
                length = int(contractor.lic_expire_date.year - contractor.lic_issue_date.year)
            elif (not contractor.lic_expire_date) and (not contractor.lic_issue_date):
                length = 0
            else:
                length = int(datetime.date.today().year - contractor.lic_issue_date.year)
        except:
            length = "N/A"
        # test issue, won't happen in prod


        try:
            complaint = ComplaintOverall.objects.get(contractor=contractor)
        except:
            complaint = Complaint1
            complaint.case = 0
            complaint.citation = 0
            complaint.arbitration = 0
            complaint.complaint = 0

        if request.user.is_anonymous():
            p_lic_num = None
        else:
            try:
                p_lic_num = str(request.user.professional_profiles.first().professional.lic_num)
            except:
                p_lic_num = None

        # other situation
        user_rating_form = UserRatingForm()
        # review_form = request.session.get('review_form', None)
        # if review_form is None:
        if request.user.is_authenticated:
            review_form = ReviewForm(initial={'first_name': request.user.first_name,
                                              'last_name': request.user.last_name,
                                              'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
        else:
            review_form = ReviewForm(initial={
                'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})

        try:
            overview = Overview.objects.get(content_type=ContentType.objects.get(model='contractor'),
                                            object_id=o_id).overview
        except:
            overview = _("""{lic_name} is a contractor company located in {csp} . The company holds a license number 
              according to {data_source}. According to real-time data analysis, this licensed contractor's hoome score 
              is {score} and is rated as {rank}. The License is verified as active when we checked last time. If you would
               like to know {lic_name} more, please contact us and we will share more information and data about this
                contractor to you.""").format(lic_name=contractor.lic_name, csp=contractor.csp, data_source=data_source,
                                              score=hscore.score, rank=letter_grade, full_state_name=full_state_name)

        overview_form = OverviewForm(initial={'overview': overview})

        info_dict = {"contractor": contractor, "bg_image": bgimage, "overview": overview, 'review': review,
                     "score": hscore.score, 'bond_history': bh, "wc_history": wh, "lic_type": lic_type,
                     "ratings": ratings, 'project_photos': project_photos, 'review_form': review_form,
                     "user_rating_form": user_rating_form, "complaint": complaint, "length": length,
                     'p_lic_num': p_lic_num, 'rank': letter_grade, 'overview_form': overview_form}

        if request.POST.get('review'):
            user_rating_form = UserRatingForm(request.POST)
            review_form = ReviewForm(request.POST)
            # TODO: assign a random password
            # TODO: validator doesn't work
            if review_form.is_valid() and user_rating_form.is_valid():
                # User = #ContentType.objects.get_for_model(settings.AUTH_USER_MODEL)

                # user = User(email=review_form.cleaned_data['email'],
                #             username=review_form.cleaned_data['email'],
                #             last_name=review_form.cleaned_data['last_name'],
                #             first_name=review_form.cleaned_data['first_name'],
                #             password=make_password("aaaaaaa"))
                # user.save()
                model_type = check_professional_type(request)
                review = review_form.save(commit=False)
                if request.user.is_authenticated():
                    review.user = request.user
                review.content_type = ContentType.objects.get(model=model_type)
                review.object_id = contractor.lic_id
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
                return render(request, 'contractor/contractor.html', {"info_dict": info_dict})
        # TODO: need to change here
        elif request.POST.get('overview'):
            edit_overview(request, contractor_id)
            return redirect(request.path)
        else:
            raise Http404(_("Error Pages!"))


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


def display_project_photos(request, contractor_id):
    if request.is_ajax() and request.method == "POST":
        contractor = Contractor.objects.get(lic_num=contractor_id)
        template_name = 'contractor/contractor_project_photo.html'
        project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='contractor'),
                                              object_id=contractor.lic_id)
        info_dict = {'project_photos': project_photos}  # , 'contractor': contractor
        return render(request, template_name, {'info_dict': info_dict})
    else:
        raise Http404(_('No Pages Found.'))


def upload_project_photos(request, contractor_id):
    if request.user.is_anonymous():
        p_lic_num = None
    else:
        try:
            p_lic_num = str(request.user.professional_profiles.first().professional.lic_num)
        except:
            p_lic_num = None
    if str(p_lic_num) == str(contractor_id):
        contractor = Contractor.objects.get(lic_num=contractor_id)
        template_name = 'contractor/contractor_project_photos_upload.html'  # Replace with your template.
        success_url = '/contractor/' + contractor_id  # Replace with your URL or reverse().

        if request.method == "POST":
            # contractor = Contractor.objects.get(lic_num=contractor_id)
            form = PhotoForm(request.POST, request.FILES)
            content_type = ContentType.objects.get(model='contractor')
            object_id = int(contractor.lic_id)
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


def delete_photo(request, contractor_id):
    if request.is_ajax() and request.method == "POST":
        if contractor_id:
            contractor_id = str(contractor_id)
        if request.user.is_anonymous():
            p_lic_num = None
        else:
            try:
                p_lic_num = str(request.user.professional_profiles.first().professional.lic_num)
            except:
                p_lic_num = None
        if str(p_lic_num) == str(contractor_id):
            data = {}

            data.update(json.loads(request.body))
            # print(data)
            photo_id = data.get('id', None)
            if photo_id is not None:
                photo = Photo.objects.get(id=photo_id)
                photo.delete()
                response_data = {'success': 'photo is deleted successfully'}

                return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)
            else:
                response_data = {'error': 'photo_id is empty'}
                return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)
        else:
            response_data = {'error', 'deletion request is not from its owner'}
            return HttpResponse(response_data, content_type='application/json', status=200)
    else:
        raise Http404
