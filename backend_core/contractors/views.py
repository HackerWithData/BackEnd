# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Count, Min, Sum, Avg
from django.shortcuts import render
from contractors.models import Contractor, BondHistory, WorkerCompensationHistory  #, EfficiencyRating #,ContractorRate
from disk.models import UserFile, ProjectImage


# Create your views here.
import datetime

def getStateFullName(state):
    FullName= "California"
    return FullName


def display_contractor(request, contractor_id):
    contractor = Contractor.objects.get(LicNum=contractor_id)
    photo = ProjectImage.objects.filter(userName=contractor.BusName)
    #print vars(photo)
    #print(UserFile.objects.get(userName=contractor.BusName).uploadFile)
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

    LicType = contractor.LicType.split(',')
    #rate = ContractorRate.objects.create(slug)
    #rate = ContractorRate.objects.get(contractor=slug)
    #queryset = Contractor.objects.filter(ratings__isnull=False).order_by('ratings__average')
    # print( vars(queryset))
    #rate = contractor.ratings.get()
    #EfficiencyRate = EfficiencyRating.objects.get_or_create(contractor=contractor)[0]

    # with connection.cursor() as cursor:
    #     cursor.execute("""Select avg(total) from star_ratings_rating
    #     where object_id in (Select id from contractors_efficiencyrating where contractor_id="%s")"""%contractor.LicNum)
    #     E_rate = cursor.fetchone()

    #E_rate = EfficiencyRate.ratings.get()
    #try:
    #E_rate = EfficiencyRating.objects.filter(contractor=contractor).annotate(Avg('ratings'))
    #print(vars(E_rate[0]),vars(E_rate[0]))
    #except:
    #    E_rate = None
    info_dict = {"contractor": contractor, 'photo': photo, "bgimage": uf, "overview": overview,
                 "Score": Score,'bondhistory': bh,"wchistory": wh,"LicType": LicType}#"rate":rate,"E_rate":E_rate,"EfficiencyRate":EfficiencyRate}
    #print(info_dict)
    return render(request, 'contractor/contractor.html', {"info_dict": info_dict})
