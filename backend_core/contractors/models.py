# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
#from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.


class Contractor(models.Model):
    LicNum = models.IntegerField(primary_key=True, unique=True)
    BusName = models.CharField(max_length=100)
    LicStatus = models.CharField(max_length=100)
    LicIssueDate = models.DateField()
    LicExpireDate = models.DateField()
    LicType = models.CharField(max_length=100)
    Entity = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    County = models.CharField(max_length=50)
    State = models.CharField(max_length=15)
    PosCode = models.IntegerField()
    Phone = models.CharField(max_length=15)
    LicStatusAdd = models.TextField()
    #ratings = GenericRelation(Rating, related_query_name='contractors')


class BondCompany(models.Model):
    SuretyCode = models.CharField(primary_key=True,max_length=10)
    SuretyName = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    County = models.CharField(max_length=50)
    State = models.CharField(max_length=15)
    PosCode = models.IntegerField()


class BondHistory(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    SuretyCode = models.ForeignKey(BondCompany, on_delete=models.CASCADE)
    SuretyCompany = models.CharField(max_length=255)
    BondNum = models.CharField(max_length=20)
    BondAmount = models.CharField(max_length=20)
    BondEffectiveDate = models.DateField()
    BondCancellationDate = models.DateField()


class InssuranceCompany(models.Model):
    InsurCode = models.CharField(primary_key=True,max_length=10)
    InsurName = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    County = models.CharField(max_length=50)
    State = models.CharField(max_length=15)
    PosCode = models.IntegerField()


class WorkerCompensationHistory(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    InsurCode = models.ForeignKey(InssuranceCompany, on_delete=models.CASCADE)
    InsurCompany = models.CharField(max_length=255)
    PolicyNum = models.CharField(max_length=20)
    InsurEffectiveDate = models.DateField()
    InsurCancellationDate = models.DateField()


class Personnel(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    Title = models.CharField(max_length=50)
    AssociationDate = models.DateField()
    LicType = models.CharField(max_length=100)


class LicenseRelation(models.Model):
    person = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name='contractor')
    RelatedContractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name='RelatedContractor')

    class Meta:
        unique_together = ('person', 'contractor', 'RelatedContractor')


# class EfficiencyRating(models.Model):
#     # user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
#     contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name='E_contractor',primary_key=True)
#     ratings = GenericRelation(Rating, related_query_name='efficiencyratings')

    # class Meta:
    #     unique_together = ('user', 'contractor',)



# class ContractorRate(models.Model):
#     bar = models.ForeignKey(Contractor, on_delete=models.CASCADE)
#     ratings = GenericRelation(Rating, related_query_name='contractorrates')
#
#     def __str__(self):
#         return self.name
