# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.
from django.http import HttpResponseNotFound
from django.shortcuts import render,redirect
from users.models import User
from review.forms import ReviewForm
from ratings.forms import UserRatingForm
from ratings.models import UserRating, Rating
from django.contrib.auth.hashers import make_password
from review.models import Review
from contractors.models import Overview
from photos.models import Photo
from django.contrib.contenttypes.models import ContentType
from photos.models import BackgroundPhoto
from photos.forms import PhotoForm
from models import Architect
import datetime
from django.utils.translation import ugettext as _
from contractors.views import submit_review, edit_overview
from django.views import View
from professionals.models import Professional
from django.contrib import messages
from contractors.forms import OverviewForm
# Create your views here.


def getStateFullName(state):
    FullName = "California"
    return FullName


# TODO: add a overview database
class ArchitectDetail(View):
    def post(self, request, o_id):
        if request.POST.get('review'):
            submit_review(request, o_id)
            return redirect(request.path)
        elif request.POST.get('overview'):
            edit_overview(request, o_id)
            return redirect(request.path)
        else:
            return HttpResponseNotFound("Error Pages!")

    def get(self, request, o_id):
        # architect info
        architect = Architect.objects.get(lic_num=o_id)
        # contractor background image
        try:
            bgimage = BackgroundPhoto.objects.get(content_type=ContentType.objects.get(model='architect'),
                                                  object_id=o_id)
        except:
            bgimage = None

        data_source = 'California Architects Board'
        score = None
        rank = None
        full_state_name = getStateFullName(architect.state)
        # preferred_project_type = 'house remodel'
        # if preferred_project_type:
        #     specialization = 'with many year experiences in ' + preferred_project_type
        # else:
        #     specialization = None

        # Lic Type
        lic_type = architect.lic_type.split('&')
        try:
            review = Review.objects.filter(content_type=ContentType.objects.get(model='architect'),
                                           object_id=o_id, review_status='A')
        except:
            review = None

        RATING_STAR_MAX = 10
        contractor_ratings = Rating.objects.filter(content_type=ContentType.objects.get(model='architect'), object_id=o_id).order_by('ratings_average')
        ratings = {}
        ratings['stars'] = range(RATING_STAR_MAX)
        def avg_rating(rt):
            s = 0
            l = 0
            if review:
                for r in review:
                    rate_list = [i.rating_score for i in r.userrating_set.all() if i.rating_type == rt]
                    s += sum(rate_list)
                    l += len(rate_list)
                return s * 1.0 / l
            else:
                return 0

        # TODO:NEED TO CHANGE HERE
        ratings['overall'] = (avg_rating('Q') + avg_rating('E') + avg_rating('L')) / 3
        try:
            ratings['rate'] = [(item.average, round(item.average * 1.0 / RATING_STAR_MAX, 2)) for item in
                               contractor_ratings]
        except:
            pass


        if request.user.is_anonymous():
            p_lic_num = None
        else:
            try:
                p_lic_num = int(request.user.professional_profiles.first().professional.lic_num)
            except:
                p_lic_num = None

        project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='architect'),
                                              object_id=o_id)
        # other situation
        user_rating_form = UserRatingForm()
        if request.user.is_authenticated:
            review_form = ReviewForm(initial={'first_name': request.user.first_name,
                                              'last_name': request.user.last_name,
                                              'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
        else:
            review_form = ReviewForm(initial={'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})

        try:
            overview = Overview.objects.get(content_type=ContentType.objects.get(model='architect'),
                                            object_id=o_id).overview
        except Overview.DoesNotExist:
            # The score of {score} ranks in the top {rank} %% of {full_state_name} licensed contractors.
            overview = _("""{bus_name} is an architect from {city}. The company holds a license number according to {data_source}. 
                The License is verified as active when we checked last time. If you would like to know {bus_name} more, 
                please contact us and we will share more information about this architect to you.
                """).format(bus_name=architect.lic_name, city=architect.city, state=architect.state,
                            data_source=data_source, score=score, rank=rank, full_state_name=full_state_name)

        overview_form = OverviewForm(initial={'overview': overview})

        info_dict = {"architect": architect, "bg_image": bgimage, "overview": overview,
                     "score": score, "lic_type": lic_type, 'review': review,
                     "ratings": ratings, 'project_photos': project_photos, 'review_form': review_form,
                     "user_rating_form": user_rating_form, 'p_lic_num': p_lic_num,'overview_form': overview_form}
        return render(request, 'architect/architect.html', {"info_dict": info_dict})


def display_project_photos(request, o_id):
    if request.is_ajax() and request.method == "POST":
        template_name = 'contractor/contractor_project_photo.html'
        architect = Architect.objects.get(lic_num=o_id)
        project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='architect'),
                                              object_id=o_id)
        info_dict = {'project_photos': project_photos, 'architect': architect}
        return render(request, template_name, {'info_dict': info_dict})
    else:
        return HttpResponseNotFound('No Pages Found.')


# %% TODO: change function to accept all instance like architects or designers
def upload_project_photos(request, o_id):
    if request.user.is_anonymous():
        p_lic_num = None
    else:
        try:
            p_lic_num = int(request.user.professional_profiles.first().professional.lic_num)
        except:
            p_lic_num = None
    if str(p_lic_num) == str(o_id):
        template_name = 'contractor/contractor_project_photos_upload.html'  # Replace with your template.
        success_url = '/architect/'+o_id  # Replace with your URL or reverse().

        if request.method == "POST":
            form = PhotoForm(request.POST, request.FILES)
            content_type = ContentType.objects.get(model='architect')
            object_id = int(o_id)
            files = request.FILES.getlist('img')
            if form.is_valid():
                if len(files) > 0:
                    for f in files:
                        instance = Photo.objects.create(img=f, title=f.name, content_type=content_type, object_id=object_id)
                        instance.save()
                else:
                    pass
                return redirect(success_url)
        form = PhotoForm()
        info_dict = {'form': form}
        return render(request, template_name, info_dict)
    else:
        return HttpResponseNotFound('No Pages Found.')