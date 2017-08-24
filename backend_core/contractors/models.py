# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Contractor(models.Model):
    LicNum = models.IntegerField(primary_key=True, unique=True)
    BusName = models.CharField()
    LicStatus = models.CharField()
    LicIssueDate = models.DateField()
    LicExpireDate = models.DateField()
    LicType = models.CharField()
    Entity = models.CharField()
    Address = models.CharField()
    County = models.CharField()
    State = models.CharField()
    PosCode = models.IntegerField()
    Phone = models.CharField()
    LicStatusAdd = models.CharField()


class BondCompany(models.Model):
    SuretyCode = models.CharField(primary_key=True)
    SuretyName = models.CharField()
    Address = models.CharField()
    County = models.CharField()
    State = models.CharField()
    PosCode = models.IntegerField()


class BondHistory(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    SuretyCode = models.ForeignKey(BondCompany, on_delete=models.CASCADE)
    BondNum = models.CharField()
    BondAmount = models.CharField()
    BondEffectiveDate = models.DateField()
    BondCancellationDate = models.DateField()


class InssuranceCompany(models.Model):
    InsurCode = models.CharField(primary_key=True)
    InsurName = models.CharField()
    Address = models.CharField()
    County = models.CharField()
    State = models.CharField()
    PosCode = models.IntegerField()


class WorkerCompensationHistory(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    InsurCode = models.ForeignKey(InssuranceCompany, on_delete=models.CASCADE)
    PolicyNum = models.CharField()
    InsurEffectiveDate = models.DateField()
    InsurCancellationDate = models.DateField()


class Personnel(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    FirstName = models.CharField()
    LastName = models.CharField()


class LicenseRelation(models.Model):
    person = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    related_contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('person', 'contractor', 'related_contractor')


