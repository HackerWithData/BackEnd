# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from django.conf import settings
from django.db import models
#from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.


#TODO：Clean Data Format
class Contractor(models.Model):
    lic_num = models.IntegerField(primary_key=True, unique=True)
    bus_name = models.CharField(max_length=255)
    lic_status = models.CharField(max_length=100, blank=True)
    lic_issue_date = models.DateField(blank=True, null=True)
    lic_expire_date = models.DateField(blank=True, null=True)
    lic_type = models.CharField(max_length=100, blank=True)
    entity = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    csp = models.CharField(max_length=62, blank=True)
    state = models.CharField(max_length=62)
    pos_code = models.CharField(max_length=62)
    phone = models.CharField(max_length=62, blank=True)
    lic_status_add = models.TextField(blank=True)
    bus_info_add = models.TextField(blank=True)
    dba = models.CharField(max_length=128, blank=True)
    #ratings = GenericRelation(Rating, related_query_name='contractors')

    # def __unicode__(self):
    #     return self.LicNum


class BondCompany(models.Model):
    surety_code = models.CharField(primary_key=True, max_length=10)
    surety_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    county = models.CharField(max_length=50)
    state = models.CharField(max_length=15)
    pos_code = models.IntegerField()


class BondHistory(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    surety_code = models.ForeignKey(BondCompany, on_delete=models.CASCADE)
    surety_company = models.CharField(max_length=255)
    bond_num = models.CharField(max_length=20)
    bond_amount = models.CharField(max_length=20)
    bond_effective_date = models.DateField()
    bond_cancellation_date = models.DateField()


class InssuranceCompany(models.Model):
    insur_code = models.CharField(primary_key=True, max_length=10)
    insur_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    county = models.CharField(max_length=50)
    state = models.CharField(max_length=15)
    pos_code = models.IntegerField()


class WorkerCompensationHistory(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    insur_code = models.ForeignKey(InssuranceCompany, on_delete=models.CASCADE, blank=True, null=True)
    insur_company = models.CharField(max_length=255)
    policy_num = models.CharField(max_length=20)
    insur_effective_date = models.DateField()
    insur_cancellation_date = models.DateField()

#TODO: name last name?
class Personnel(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    #first_name = models.CharField(max_length=30)
    name = models.CharField(max_length=60)
    #last_name = models.CharField(max_length=30)
    title = models.CharField(max_length=50)
    association_date = models.DateField()
    deassociation_date = models.DateField()
    lic_type = models.CharField(max_length=100)

#TODO: match with person with Personnel table
class LicenseRelation(models.Model):
    name = models.CharField(max_length=100)
    #person = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name='contractor')
    related_contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name='related_contractor')

    class Meta:
        unique_together = ('name', 'contractor', 'related_contractor')


# class EfficiencyRating(models.Model):
#     # user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
#     contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, related_name='E_contractor',primary_key=True)
#     ratings = GenericRelation(Rating, related_query_name='efficiencyratings')

    #class Meta:
    #    unique_together = ('user', 'contractor',)


# class ContractorRate(models.Model):
#     bar = models.ForeignKey(Contractor, on_delete=models.CASCADE)
#     ratings = GenericRelation(Rating, related_query_name='contractorrates')
#
#     def __str__(self):
#         return self.name
