# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#TODO：Clean Data Format
class Contractor(models.Model):
    lic_id = models.AutoField(primary_key=True)
    lic_num = models.CharField(max_length=63)
    lic_type = models.CharField(blank=True, null=True,max_length=1000)
    lic_name = models.CharField(max_length=255,blank=True, null=True)
    lic_status = models.CharField(max_length=30,blank=True, null=True)
    lic_issue_date = models.DateField(null=True)
    lic_expire_date = models.DateField(null=True)
    entity = models.CharField(max_length=25,blank=True, null=True)
    street_address = models.CharField(max_length=255,blank=True, null=True)
    csp = models.CharField(max_length=63, blank=True, null=True)
    state = models.CharField(max_length=63, blank=True, null=True)
    pos_code = models.CharField(max_length=25, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    lic_status_add = models.TextField(blank=True, null=True)
    bus_info_add = models.TextField(blank=True, null=True)
    dba = models.CharField(max_length=255, blank=True, null=True)
    uuid = models.CharField(max_length=36, default='0')
    license_board = models.CharField(max_length=255, blank=True, null=True, default='California Contractor State License Board')

    class Meta:
        unique_together = ('lic_num', 'lic_type','license_board')

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


class InsuranceCompany(models.Model):
    insur_code = models.CharField(primary_key=True, max_length=10)
    insur_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    county = models.CharField(max_length=63)
    state = models.CharField(max_length=63)
    pos_code = models.CharField(max_length=25, blank=True, null=True)


class WorkerCompensationHistory(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING)
    insur_code = models.ForeignKey(InsuranceCompany, on_delete=models.DO_NOTHING, blank=True, null=True)
    insur_company = models.CharField(max_length=255)
    policy_num = models.CharField(max_length=20)
    insur_effective_date = models.DateField(blank=True, null=True)
    insur_cancellation_date = models.DateField(blank=True, null=True)


#TODO: name last name?
class Personnel(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=63)
    title = models.CharField(max_length=63)
    association_date = models.DateField()
    deassociation_date = models.DateField()
    lic_type = models.CharField(max_length=63)


#TODO: match with person with Personnel table Need to reset db . had a problem in FK
class LicenseRelation(models.Model):
    name = models.CharField(max_length=63)
    #Do not use the reference below because it will requite name_id which is not necessary in this case
    #name = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING, related_name='contractor')
    related_contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING, related_name='related_contractor')

    class Meta:
        unique_together = ('name', 'contractor', 'related_contractor')


class Complaint(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING)
    complaint_type = models.CharField(max_length=255)
    complain_num = models.CharField(max_length=255)
    time = models.DateField()
    result = models.CharField(max_length=255)
    complaint_count = models.IntegerField(null=True, blank=False)
    code_source = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    code_detail = models.CharField(max_length=255)
    doc_link = models.CharField(max_length=255)


class ComplaintOverall(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING)
    case = models.IntegerField(null=True, blank=False)
    citation = models.IntegerField(null=True, blank=False)
    arbitration = models.IntegerField(null=True, blank=False)
    complaint = models.IntegerField(null=True, blank=False)


