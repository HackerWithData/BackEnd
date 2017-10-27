# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from django.conf import settings
from django.db import models
#from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from tinymce import models as tinymce_models
# Create your models here.


#TODO：Clean Data Format
class Contractor(models.Model):
    lic_num = models.IntegerField(primary_key=True, unique=True)
    lic_name = models.CharField(max_length=255)
    lic_status = models.CharField(max_length=30)
    lic_issue_date = models.DateField(blank=True, null=True)
    lic_expire_date = models.DateField(blank=True, null=True)
    lic_type = models.TextField()
    entity = models.CharField(max_length=25)
    street_address = models.CharField(max_length=255)
    csp = models.CharField(max_length=63, blank=True)
    state = models.CharField(max_length=63)
    pos_code = models.CharField(max_length=25)
    phone = models.CharField(max_length=25, blank=True, null=True)
    lic_status_add = models.TextField(blank=True, null=True)
    bus_info_add = models.TextField(blank=True, null=True)
    dba = models.CharField(max_length=255, blank=True, null=True)

    #ratings = GenericRelation(Rating, related_query_name='contractors')

    def __iter__(self):
        return self.__dict__.iteritems()


class BondCompany(models.Model):
    surety_code = models.CharField(primary_key=True, max_length=10)
    surety_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=63, blank=True, null=True)
    state = models.CharField(max_length=63, blank=True, null=True)
    pos_code = models.CharField(max_length=25, blank=True, null=True)


class BondHistory(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING)
    surety_code = models.ForeignKey(BondCompany, on_delete=models.DO_NOTHING, blank=True, null=True)
    surety_company = models.CharField(max_length=255)
    bond_num = models.CharField(max_length=20)
    bond_amount = models.CharField(max_length=20)
    bond_effective_date = models.DateField(blank=True, null=True)
    bond_cancellation_date = models.DateField(blank=True, null=True)


class InssuranceCompany(models.Model):
    insur_code = models.CharField(primary_key=True, max_length=10)
    insur_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    county = models.CharField(max_length=63)
    state = models.CharField(max_length=63)
    pos_code = models.CharField(max_length=25, blank=True, null=True)


class WorkerCompensationHistory(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING)
    insur_code = models.ForeignKey(InssuranceCompany, on_delete=models.DO_NOTHING, blank=True, null=True)
    insur_company = models.CharField(max_length=255)
    policy_num = models.CharField(max_length=20)
    insur_effective_date = models.DateField(blank=True, null=True)
    insur_cancellation_date = models.DateField(blank=True, null=True)

#TODO: name last name?
class Personnel(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING)
    #first_name = models.CharField(max_length=30)
    name = models.CharField(max_length=63)
    #last_name = models.CharField(max_length=30)
    title = models.CharField(max_length=63)
    association_date = models.DateField()
    deassociation_date = models.DateField()
    lic_type = models.CharField(max_length=63)

#TODO: match with person with Personnel table Need to reset db . had a problem in FK
class LicenseRelation(models.Model):
    name = models.CharField(max_length=63)
    #Do not use the reference below because it will requite name_id which is necessary in this case
    #name = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING, related_name='contractor')
    related_contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING, related_name='related_contractor')

    class Meta:
        unique_together = ('name', 'contractor', 'related_contractor')

class Complaint(models.Model):
    lic_num = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING)
    complaint_type = models.CharField(max_length=255,null=False, blank=False)
    complain_num = models.CharField(max_length=255)
    time = models.DateField()
    result = models.CharField(max_length=255)
    complaint_count = models.IntegerField(null=True, blank=False)
    code_source = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    code_detail = models.CharField(max_length=255)
    doc_link = models.CharField(max_length=255)

class Complaint_Overall(models.Model):
    lic_num = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING)
    case = models.IntegerField(null=True, blank=False)
    citation = models.IntegerField(null=True, blank=False)
    arbitration = models.IntegerField(null=True, blank=False)
    complaint = models.IntegerField(null=True, blank=False)


class Overview(models.Model):
    overview = tinymce_models.HTMLField()
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')