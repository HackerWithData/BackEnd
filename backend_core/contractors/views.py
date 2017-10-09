# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseNotFound
from django.shortcuts import render
from contractors.models import Contractor, BondHistory, WorkerCompensationHistory  # , EfficiencyRating #,ContractorRate
from users.models import User
from review.forms import ReviewForm
from ratings.forms import UserRatingForm
from ratings.models import UserRating, Rating
from django.contrib.auth.hashers import make_password
from contractors.models import Contractor
from review.models import Review
from hscore.models import Hscore
from photos.models import Photo
from django.contrib.contenttypes.models import ContentType
from photos.models import BackgroundPhoto
from photos.forms import PhotoForm
import datetime
from django.utils.translation import ugettext as _


# Create your views here.



def getStateFullName(state):
    FullName = "California"
    return FullName


# TODO: add a overview database
def display_contractor(request, contractor_id):
    o_id = contractor_id
    if request.method == "POST":

        user_rating_form = UserRatingForm(request.POST)
        # sign_up_form = SignUpForm2(request.POST)
        review_form = ReviewForm(request.POST)
        # TODO: assign a random password
        if review_form.is_valid() and user_rating_form.is_valid():
            # User = #ContentType.objects.get_for_model(settings.AUTH_USER_MODEL)

            user = User(email=review_form.cleaned_data['email'],
                        username=review_form.cleaned_data['email'],
                        last_name=review_form.cleaned_data['last_name'],
                        first_name=review_form.cleaned_data['first_name'],
                        password=make_password("aaaaaaa"))
            user.save()
            if 'contractor' in request.path:
                model_type = 'contractor'
            elif 'designer' in request.path:
                model_type = 'designer'
            elif 'architect' in request.path:
                model_type = 'architect'
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
            return render(request, 'disk/uploadsuccess.html')

    # other situation
    user_rating_form = UserRatingForm()
    if request.user.is_authenticated:
        review_form = ReviewForm(initial={'first_name': request.user.first_name,
                                          'last_name': request.user.last_name,
                                          'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})
    else:
        review_form = ReviewForm(initial={
            'project_date': datetime.datetime.today().strftime('%Y-%m-%d')})

    # contractor info
    contractor = Contractor.objects.get(lic_num=contractor_id)
    # #project photo
    # project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='contractor'), object_id=contractor_id)
    # contractor background image
    try:
        bgimage = BackgroundPhoto.objects.get(content_type=ContentType.objects.get(model='contractor'),
                                              object_id=contractor_id)
    except:
        bgimage = None

    bh_set = BondHistory.objects.filter(contractor_id=contractor_id).order_by('-bond_effective_date')
    bh = None
    if len(bh_set) > 0:
        bh = bh_set[0]

    wh_set = WorkerCompensationHistory.objects.filter(contractor_id=contractor_id).order_by('-insur_effective_date')
    wh = None
    if len(wh_set) > 0:
        wh = wh_set[0]

    data_source = 'California Contractors State License Board'
    hscore = Hscore.objects.get(content_type=ContentType.objects.get(model='contractor'),
                              object_id=contractor_id)


    rank = str(round(hscore.rank*100.0 / hscore.max,2))+"%"
    #print(hscore.rank*1.0 / hscore.max)

    full_state_name = getStateFullName(contractor.state)
    # preferred_project_type = 'house remodel'
    # if preferred_project_type:
    #     specialization = 'with many year experiences in ' + preferred_project_type
    # else:
    #     specialization = None

    overview = None
    if overview:
        pass
    else:
        overview = _("""{bus_name} is a contractor company located in {csp} . 
    The company holds a license number according to {data_source}. The score of {score} ranks in the top {rank} %% of {full_state_name} licensed contractors.
    The License is verified as active when we checked last time. If you consider to hire {bus_name}, 
    we suggest double-checking the license status and contact through us.
    """).format(bus_name=contractor.bus_name, csp=contractor.csp, data_source=data_source, score=score, rank=rank,
                full_state_name=full_state_name)

    # ,contractor.bus_name
    # Lic Type
    lic_type = contractor.lic_type.split('&')
    # review
    # if 'contractor' in request.path:
    #     model_type = 'contractor'
    # elif 'designer' in request.path:
    #     model_type = 'designer'
    # elif 'architect' in request.path:
    #     model_type = 'architect'

    try:
        review = Review.objects.filter(content_type=ContentType.objects.get(model='contractor'),
                                       object_id=contractor_id,
                                       review_status='A')
    except:
        review = None

    RATING_STAR_MAX = 10
    contractor_ratings = Rating.objects.filter(content_type=ContentType.objects.get(model='contractor'),
                                               object_id=contractor_id).order_by('ratings_average')
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
    # {'Quality': avg_rating('Q'),'Efficiency': avg_rating('E'),'Length': avg_rating('L')} #mean(contractor_ratings)*1.0/RATING_STAR_MAX
    try:
        ratings['rate'] = [(item.average, round(item.average * 1.0 / RATING_STAR_MAX, 2)) for item in
                           contractor_ratings]
    except:
        pass

    project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='contractor'),
                                          object_id=contractor_id)

    info_dict = {"contractor": contractor, "bg_image": bgimage, "overview": overview,
                 "score": score, 'bond_history': bh, "wc_history": wh, "lic_type": lic_type, 'review': review,
                 "ratings": ratings, 'project_photos': project_photos, 'review_form': review_form,
                 "user_rating_form": user_rating_form, }

    return render(request, 'contractor/contractor.html', {"info_dict": info_dict})


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
        template_name = 'contractor/contractor_project_photo.html'

        project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='contractor'),
                                              object_id=contractor_id)
        info_dict = {'project_photos': project_photos}  # , 'contractor': contractor
        return render(request, template_name, {'info_dict': info_dict})
    else:
        return HttpResponseNotFound('No Pages Found.')


def upload_project_photos(request, contractor_id):
    template_name = 'contractor/contractor_project_photos_upload.html'  # Replace with your template.
    success_url = 'disk/uploadsuccess.html'  # Replace with your URL or reverse().

    if request.method == "POST":
        # contractor = Contractor.objects.get(lic_num=contractor_id)
        form = PhotoForm(request.POST, request.FILES)
        content_type = ContentType.objects.get(model='contractor')
        object_id = int(contractor_id)
        files = request.FILES.getlist('img')
        if form.is_valid():
            if len(files) > 0:
                for f in files:
                    instance = Photo.objects.create(img=f, title=f.name, content_type=content_type, object_id=object_id)
                    instance.save()
            else:
                pass
            return render(request, success_url)
    form = PhotoForm()
    info_dict = {'form': form}
    return render(request, template_name, info_dict)

    # class ProjectPhotosUpload(View):
    #     def get(self, request, contractor_id):
    #         #photos_list = Photo.objects.all()
    #         return render(self.request, 'photos/upload_photo.html')
    #
    #     def post(self, request, contractor_id):
    #         form = PhotoForm(self.request.POST, self.request.FILES)
    #
    #         if form.is_valid():
    #             f = form.save(commit=False)
    #             contractor = Contractor.objects.get(pk='1025362')
    #             f.content_type = ContentType.objects.get(model='contractor')
    #             f.object_id = contractor.LicNum
    #             f.save()
    #             data = {'is_valid': True, 'name': f.img.name, 'url': f.img.url}
    #         else:
    #             data = {'is_valid': False}
    #         return JsonResponse(data)
