# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Count, Min, Sum, Avg
from django.shortcuts import render
from contractors.models import Contractor, BondHistory, WorkerCompensationHistory  #, EfficiencyRating #,ContractorRate
from disk.models import UserFile, ProjectImage
from review.models import Review
from ratings.models import UserRating,Rating

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

    #bond history
    bh = BondHistory.objects.filter(contractor_id=contractor_id).order_by('-BondEffectiveDate')[0]
    #work compensation history
    wh = WorkerCompensationHistory.objects.filter(contractor_id=contractor_id).order_by('-InsurEffectiveDate')[0]

    #description
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
        rating.total = rating.total + ur.rating_score
        rating.count = rating.count + 1
        rating.average = round(rating.total*1.0/rating.count, 2)
    return render(request, '/')
