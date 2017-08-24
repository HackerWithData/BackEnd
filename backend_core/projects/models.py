# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Projects(models.Model):
    ProjectId = models.BigAutoField(primary_key=True)
    contractor = models.ForeignKey('Contractors.Contractor', on_delete=models.CASCADE)
    client = models.ForeignKey('Contractors.Client', on_delete=models.CASCADE)
    ProjectType = models.CharField()
    Address = models.CharField()
    County = models.CharField()
    State = models.CharField()
    PosCode = models.IntegerField()

    class Meta:
        unique_together = ('ProjectId', 'contractor', 'client')