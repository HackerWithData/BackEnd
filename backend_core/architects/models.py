# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#TODO: please change the type of field
class Architect(models.Model):
    lic_num = models.CharField(primary_key=True, unique=True,max_length=64)
    name = models.CharField(max_length=64)
    lic_type = models.CharField(max_length=64)
    lic_status = models.CharField(max_length=64)
    issue_date = models.DateField()
    expire_date = models.DateField()
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    zip = models.CharField(max_length=64)
    county = models.CharField(max_length=64)
    actions = models.CharField(max_length=64)