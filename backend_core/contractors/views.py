# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Count, Min, Sum, Avg
from django.shortcuts import render
from contractors.models import Contractor, BondHistory, WorkerCompensationHistory  #, EfficiencyRating #,ContractorRate
from disk.models import UserFile, ProjectImage
from review.models import Review
from ratings.models import UserRating,Rating
from photos.models import Photo
from django.contrib.contenttypes.models import ContentType
from django.views import View
from photos.forms import PhotoForm
from django.http import JsonResponse
# Create your views here.
import datetime

def getStateFullName(state):
    FullName= "California"
    return FullName


def display_contractor(request, contractor_id):
    #contractor info
    contractor = Contractor.objects.get(LicNum=contractor_id)
    #project photo
    photo = ProjectImage.objects.filter(userName=contractor.BusName)
    #print vars(photo)
    #print(UserFile.objects.get(userName=contractor.BusName).uploadFile)

    #contractor background image
    try:
        uf = UserFile.objects.get(userName=contractor.BusName).uploadFile
    except:
        uf = None

    bh_set = BondHistory.objects.filter(contractor_id=contractor_id).order_by('-BondEffectiveDate')
    bh = None
    if len(bh_set) > 0:
        bh = bh_set[0]

    wh_set = WorkerCompensationHistory.objects.filter(contractor_id=contractor_id).order_by('-InsurEffectiveDate')
    wh = None
    if len(wh_set) > 0:
        wh = wh_set[0]

    DataSource = 'California Contractors State License Board'
    Score = 91
    Rank = 5
    FullStateName = getStateFullName(contractor.State)
    MostProjectType = 'house remodel'
    if MostProjectType:
        Specialization = 'with many year experiences in ' + MostProjectType
    else:
        Specialization = None

    overview = None
    if overview:
        pass
    else:
        overview = """%s is a contractor company located in %s, %s %s . 
        The company holds a license number according to %s. The score of %d ranks in the top %d %% of %s licensed contractors.
        Their License is verified as active when we checked last time. If you consider to hire Hooke Installations, 
        we suggest double-checking their license status and contact them through us.
        """%(contractor.BusName, contractor.County, contractor.State, Specialization, DataSource, Score, Rank, FullStateName)
    # Lic Type
    LicType = contractor.LicType.split(',')
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
        ratings['rate'] = [(item.average,round(item.average*1.0/RATING_STAR_MAX,2)) for item in contractor_ratings]
    except:
        pass

    info_dict = {"contractor": contractor, 'photo': photo, "bgimage": uf, "overview": overview,
                 "Score": Score, 'bondhistory': bh, "wchistory": wh, "LicType": LicType, 'review': review, "ratings": ratings}#"rate":rate,"E_rate":E_rate,"EfficiencyRate":EfficiencyRate}

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
    template_name = 'contractor/contractor_project_photo.html'
    contractor = Contractor.objects.get(LicNum=contractor_id)
    project_photos = Photo.objects.filter(content_type=ContentType.objects.get(model='contractor'), object_id=contractor_id)
    #print(project_photos)
    info_dict = {'project_photos': project_photos, 'contractor': contractor}

    return render(request, template_name, {'info_dict': info_dict})

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