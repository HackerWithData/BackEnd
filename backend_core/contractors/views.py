# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Count, Min, Sum, Avg
from django.shortcuts import render
from contractors.models import Contractor, BondHistory, WorkerCompensationHistory , EfficiencyRating #,ContractorRate
from disk.models import UserFile, ProjectImage
from django.db import connection

# Create your views here.
import datetime

def getStateFullName(sate):
    FullName= "California"
    return FullName


def display_contractor(request, contracotr_id):
    #slug = '1025362'
    contractor = Contractor.objects.get(LicNum=contracotr_id)
    photo = ProjectImage.objects.filter(userName=contractor.BusName)
    #print vars(photo)
    #print(UserFile.objects.get(userName=contractor.BusName).uploadFile)
    uf = UserFile.objects.get(userName=contractor.BusName).uploadFile


    bh = BondHistory.objects.filter(contractor_id=contracotr_id).order_by('-BondEffectiveDate')[0]
    wh = WorkerCompensationHistory.objects.filter(contractor_id=contracotr_id).order_by('-InsurEffectiveDate')[0]
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

    LicType = contractor.LicType.split(',')
    #rate = ContractorRate.objects.create(slug)
    #rate = ContractorRate.objects.get(contractor=slug)
    #queryset = Contractor.objects.filter(ratings__isnull=False).order_by('ratings__average')
    # print( vars(queryset))
    rate = contractor.ratings.get()
    EfficiencyRate = EfficiencyRating.objects.get_or_create(contractor=contractor)[0]

    # with connection.cursor() as cursor:
    #     cursor.execute("""Select avg(total) from star_ratings_rating
    #     where object_id in (Select id from contractors_efficiencyrating where contractor_id="%s")"""%contractor.LicNum)
    #     E_rate = cursor.fetchone()

    E_rate = EfficiencyRate.ratings.get()
    #try:
    #E_rate = EfficiencyRating.objects.filter(contractor=contractor).annotate(Avg('ratings'))
    #print(vars(E_rate[0]),vars(E_rate[0]))
    #except:
    #    E_rate = None
    info_dict = {"contractor": contractor, 'photo': photo, "bgimage": uf, "overview": overview,
                 "Score": Score,'bondhistory': bh,"wchistory": wh,"LicType": LicType,"rate":rate,"E_rate":E_rate,"EfficiencyRate":EfficiencyRate}

    return render(request, 'contractor/contractor.html', {"info_dict": info_dict})
