# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#TODO: please change the type of field
class Architect(models.Model):
    lic_num = models.IntegerField(primary_key=True, unique=True)
    lic_prefix = models.CharField(max_length=2)
    lic_name = models.CharField(max_length=63)
    #TODO: Consider to delete lic_type. may not be necesaary
    lic_type = models.CharField(max_length=10)
    lic_status = models.CharField(max_length=63)
    issue_date = models.DateField(null=True, blank=True)
    expire_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=63)
    county = models.CharField(max_length=63)
    state = models.CharField(max_length=63)
    country = models.CharField(max_length=63)
    zip = models.CharField(max_length=25)
    actions = models.CharField(max_length=63)

    def __iter__(self):
        return self.__dict__.iteritems()
