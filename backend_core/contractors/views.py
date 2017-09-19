# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseNotFound
from django.shortcuts import render
from contractors.models import Contractor, BondHistory, WorkerCompensationHistory  #, EfficiencyRating #,ContractorRate

from review.models import Review
from ratings.models import UserRating, Rating
from photos.models import Photo
from django.contrib.contenttypes.models import ContentType
from photos.models import BackgroundPhoto
from photos.forms import PhotoForm
import datetime
# Create your views here.



def getStateFullName(state):
    FullName= "California"
    return FullName

# TODO: add a overview database
def display_contractor(request, contractor_id):
    #contractor info
    contractor = Contractor.objects.get(lic_num=contractor_id)
    # #project photo
    # project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='contractor'), object_id=contractor_id)
    #contractor background image
    try:
        bgimage = BackgroundPhoto.objects.get(content_type=ContentType.objects.get(model='contractor'), object_id=contractor_id)
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
    score = 91
    rank = 5
    full_state_name = getStateFullName(contractor.state)
    preferred_project_type = 'house remodel'
    if preferred_project_type:
        specialization = 'with many year experiences in ' + preferred_project_type
    else:
        specialization = None

    overview = None
    if overview:
        pass
    else:
        overview = """%s is a contractor company located in %s %s . 
        The company holds a license number according to %s. The score of %d ranks in the top %d %% of %s licensed contractors.
        Their License is verified as active when we checked last time. If you consider to hire Hooke Installations, 
        we suggest double-checking their license status and contact them through us.
        """%(contractor.bus_name, contractor.csp, specialization, data_source, score, rank, full_state_name)
    # Lic Type
    lic_type = contractor.lic_type.split('&')
    #review
    try:
        review = Review.objects.filter(contractor=contractor, review_status='A')
    except:
        review = None

    RATING_STAR_MAX = 10
    contractor_ratings = Rating.objects.filter(contractor=contractor).order_by('ratings_average')
    ratings = {}
    ratings['stars'] = range(RATING_STAR_MAX)
    ratings['overall'] = ([5, 5 * 1.0 / 10],)  # (mean(contractor_ratings),mean(contractor_ratings)*1.0/RATING_STAR_MAX)
    try:
        ratings['rate'] = [(item.average,round(item.average*1.0/RATING_STAR_MAX, 2)) for item in contractor_ratings]
    except:
        pass

    info_dict = {"contractor": contractor, "bg_image": bgimage, "overview": overview,
                 "score": score, 'bond_history': bh, "wc_history": wh, "lic_type": lic_type, 'review': review,
                 "ratings": ratings}

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
        rating.average = round(rating.total*1.0/rating.count, 2)
    return render(request, '/')


def display_project_photos(request, contractor_id):
    if request.is_ajax() and request.method == "POST":
        template_name = 'contractor/contractor_project_photo.html'
        contractor = Contractor.objects.get(lic_num=contractor_id)
        project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='contractor'), object_id=contractor_id)
        info_dict = {'project_photos': project_photos, 'contractor': contractor}
        # if request.is_ajax():
        #     html = render_to_string(template_name, {'info_dict': info_dict})
        #     return HttpResponse(html)
        # else:
        return render(request, template_name, {'info_dict': info_dict})
    else:
        return HttpResponseNotFound('No Pages Found.')


def upload_project_photos(request, contracotr_id):
    template_name = 'contractor/contractor_project_photos_upload.html'  # Replace with your template.
    success_url = 'disk/uploadsuccess.html'  # Replace with your URL or reverse().

    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        content_type = ContentType.objects.get(model='contractor')
        object_id = int(contracotr_id)
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