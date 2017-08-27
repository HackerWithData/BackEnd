# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from contractors.models import Contractor, BondHistory, WorkerCompensationHistory
from disk.models import UserFile, ProjectImage
# Create your views here.
import datetime

def getStateFullName(sate):
    FullName= "California"
    return FullName


def display_contractor(request, slug):
    slug = '1025362'
    contractor = Contractor.objects.get(LicNum=slug)
    photo = ProjectImage.objects.filter(userName=contractor.BusName)
    #print vars(photo)
    #print(UserFile.objects.get(userName=contractor.BusName).uploadFile)
    uf = UserFile.objects.get(userName=contractor.BusName).uploadFile


    bh = BondHistory.objects.filter(contractor_id=slug).order_by('-BondEffectiveDate')[0]
    wh = WorkerCompensationHistory.objects.filter(contractor_id=slug).order_by('-InsurEffectiveDate')[0]
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

    info_dict = {"contractor": contractor, 'photo': photo, "bgimage": uf, "overview": overview,
                 "Score": Score,'bondhistory': bh,"wchistory": wh,"LicType": LicType}

    return render(request, 'contractor/contractor.html', {"info_dict": info_dict})
