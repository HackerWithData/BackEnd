# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from contractors.models import Contractor
# Create your models here.
class Review(models.Model):
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 25)
    project_date = models.DateField()
    project_address = models.CharField(max_length=100)
    project_zipcode = models.CharField(max_length=20)
    project_cost = models.IntegerField()
    project_duration = models.IntegerField()
    comments = models.TextField()
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
