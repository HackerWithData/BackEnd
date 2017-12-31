# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.utils.translation import ugettext as _, ugettext_lazy as _
from django.views import View
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType


from ratings.forms import UserRatingForm
from ratings.models import UserRating, Rating
from review.forms import ReviewForm
from review.models import Review
from photos.models import Photo
from photos.models import BackgroundPhoto
from photos.forms import PhotoForm
from contractors.utils import convert_hscore_to_rank, get_state_full_name, avg_rating
from overviews.models import Overview
from overviews.forms import OverviewForm
from overviews.views import edit_overview
from professionals.utils import check_professional_type

from .models import Designer
# Create your views here.



# TODO: add a overview database
class DesignerDetail(View):
    def post(self, request, designer_id):
        designer = Designer.objects.get(lic_num=str(designer_id))
        o_id = designer.lic_id
        try:
            bgimage = BackgroundPhoto.objects.get(content_type=ContentType.objects.get(model='designer'),
                                                  object_id=o_id)
        except:
            bgimage = None

        data_source = 'NCIQ'
        score = None
        rank = None

        full_state_name = get_state_full_name(designer.state)
        # preferred_project_type = 'house remodel'
        # if preferred_project_type:
        #     specialization = 'with many year experiences in ' + preferred_project_type
        # else:
        #     specialization = None
        # Lic Type
        lic_type = designer.lic_type.split('&')
        try:
            review = Review.objects.filter(content_type=ContentType.objects.get(model='designer'),
                                           object_id=o_id,
                                           review_status='A')
        except:
            review = None

        RATING_STAR_MAX = 10
        contractor_ratings = Rating.objects.filter(content_type=ContentType.objects.get(model='designer'),
                                                   object_id=o_id).order_by('ratings_average')
        ratings = {}
        ratings['stars'] = range(RATING_STAR_MAX, 0, -1)

        # TODO:NEED TO CHANGE HERE
        ratings['overall'] = (avg_rating(review, 'Q') + avg_rating(review, 'E') + avg_rating(review, 'L')) / 3
        try:
            ratings['rate'] = [(item.average, round(item.average * 1.0 / RATING_STAR_MAX, 2)) for item in
                               contractor_ratings]
        except:
            pass

        if request.user.is_anonymous():
            p_lic_num = None
        else:
            try:
                p_lic_num = str(request.user.professional_profiles.first().professional.lic_num)
            except:
                p_lic_num = None

        project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='designer'),
                                              object_id=o_id)

        user_rating_form = UserRatingForm()
        if request.user.is_authenticated:
            review_form = ReviewForm(initial={'first_name': request.user.first_name,
                                              'last_name': request.user.last_name,
                                              'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
        else:
            review_form = ReviewForm(initial={'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})

        try:
            overview = Overview.objects.get(content_type=ContentType.objects.get(model='designer'),
                                            object_id=o_id).overview
        except Overview.DoesNotExist:
            overview = _("""{bus_name} is a designer based on {city} {state} . The company holds a license number according to {data_source}. 
                The License is verified as active when we checked last time. If you would like to know {bus_name} more, 
                please contact us and we will share more information about this designer to you.
                """).format(bus_name=designer.lic_name, city=designer.city, state=designer.state,
                            data_source=data_source,
                            rank=rank, full_state_name=full_state_name)

        overview_form = OverviewForm(initial={'overview': overview})

        info_dict = {"designer": designer, "bg_image": bgimage, "overview": overview,
                     "score": score, "lic_type": lic_type, 'review': review,
                     "ratings": ratings, 'project_photos': project_photos, 'review_form': review_form,
                     "user_rating_form": user_rating_form, 'overview_form': overview_form, 'p_lic_num': p_lic_num}
        if request.POST.get('review'):
            user_rating_form = UserRatingForm(request.POST)
            review_form = ReviewForm(request.POST)
            # TODO: assign a random password
            # TODO: validator doesn't work
            if review_form.is_valid() and user_rating_form.is_valid():
                model_type = check_professional_type(request)
                review = review_form.save(commit=False)
                if request.user.is_authenticated():
                    review.user = request.user
                review.content_type = ContentType.objects.get(model=model_type)
                review.object_id = designer.lic_id
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
                return render(request, 'designer/designer.html', {"info_dict": info_dict})
        elif request.POST.get('overview'):
            edit_overview(request, o_id)
            return redirect(request.path)
        else:
            raise Http404("Error Pages!")

    def get(self, request, designer_id):
        designer = Designer.objects.get(lic_num=str(designer_id))
        o_id = designer.lic_id
        try:
            bgimage = BackgroundPhoto.objects.get(content_type=ContentType.objects.get(model='designer'),
                                                  object_id=o_id)
        except:
            bgimage = None

        data_source = 'NCIQ'
        score = None
        rank = None

        full_state_name = get_state_full_name(designer.state)
        # preferred_project_type = 'house remodel'
        # if preferred_project_type:
        #     specialization = 'with many year experiences in ' + preferred_project_type
        # else:
        #     specialization = None
        # Lic Type
        lic_type = designer.lic_type.split('&')
        try:
            review = Review.objects.filter(content_type=ContentType.objects.get(model='designer'),
                                           object_id=o_id,
                                           review_status='A')
        except:
            review = None

        RATING_STAR_MAX = 10
        contractor_ratings = Rating.objects.filter(content_type=ContentType.objects.get(model='designer'),
                                                   object_id=o_id).order_by('ratings_average')
        ratings = {}
        ratings['stars'] = range(RATING_STAR_MAX, 0, -1)

        # TODO:NEED TO CHANGE HERE
        ratings['overall'] = (avg_rating(review, 'Q') + avg_rating(review, 'E') + avg_rating(review, 'L')) / 3
        try:
            ratings['rate'] = [(item.average, round(item.average * 1.0 / RATING_STAR_MAX, 2)) for item in
                               contractor_ratings]
        except:
            pass

        if request.user.is_anonymous():
            p_lic_num = None
        else:
            try:
                p_lic_num = str(request.user.professional_profiles.first().professional.lic_num)
            except:
                p_lic_num = None

        project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='designer'),
                                              object_id=o_id)

        user_rating_form = UserRatingForm()
        if request.user.is_authenticated:
            review_form = ReviewForm(initial={'first_name': request.user.first_name,
                                              'last_name': request.user.last_name,
                                              'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
        else:
            review_form = ReviewForm(initial={'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})

        try:
            overview = Overview.objects.get(content_type=ContentType.objects.get(model='designer'),
                                            object_id=o_id).overview
        except Overview.DoesNotExist:
            overview = _("""{bus_name} is a designer based on {city} {state} . The company holds a license number according to {data_source}. 
                The License is verified as active when we checked last time. If you would like to know {bus_name} more, 
                please contact us and we will share more information about this designer to you.
                """).format(bus_name=designer.lic_name, city=designer.city, state=designer.state,
                            data_source=data_source,
                            rank=rank, full_state_name=full_state_name)

        overview_form = OverviewForm(initial={'overview': overview})

        info_dict = {"designer": designer, "bg_image": bgimage, "overview": overview,
                     "score": score, "lic_type": lic_type, 'review': review,
                     "ratings": ratings, 'project_photos': project_photos, 'review_form': review_form,
                     "user_rating_form": user_rating_form, 'overview_form': overview_form, 'p_lic_num': p_lic_num}
        return render(request, 'designer/designer.html', {"info_dict": info_dict})


def display_project_photos(request, o_id):
    if request.is_ajax() and request.method == "POST":
        template_name = 'designer/designer_project_photo.html'
        designer = Designer.objects.get(lic_num=o_id)
        project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='designer'),
                                              object_id=designer.lic_id)
        info_dict = {'project_photos': project_photos, 'designer': designer}
        return render(request, template_name, {'info_dict': info_dict})
    else:
        raise Http404('No Pages Found.')


# %% TODO: change function to accept all instance like architects or designers
def upload_project_photos(request, o_id):
    if request.user.is_anonymous():
        p_lic_num = None
    else:
        try:
            p_lic_num = str(request.user.professional_profiles.first().professional.lic_num)
        except:
            p_lic_num = None

    if str(p_lic_num) == str(o_id):
        designer = Designer.objects.get(lic_num=o_id)
        template_name = 'designer/designer_project_photos_upload.html'  # Replace with your template.
        success_url = '/designer/' + o_id  # Replace with your URL or reverse().

        if request.method == "POST":
            form = PhotoForm(request.POST, request.FILES)
            content_type = ContentType.objects.get(model='designer')
            files = request.FILES.getlist('img')
            if form.is_valid():
                if len(files) > 0:
                    for f in files:
                        instance = Photo.objects.create(img=f, title=f.name, content_type=content_type,
                                                        object_id=int(designer.lic_id))
                        instance.save()
                else:
                    pass
                return redirect(success_url)
        form = PhotoForm()
        info_dict = {'form': form}
        return render(request, template_name, info_dict)
    else:
        raise Http404('No Pages Found.')
