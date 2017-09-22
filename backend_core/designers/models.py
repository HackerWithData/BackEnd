# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#TODO: please change the type of field
class Designer(models.Model):

    lic_num = models.IntegerField(primary_key=True, unique=True)
    website = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)
    email = models.CharField(max_length=15)
    bus_name = models.CharField(max_length=15)
    office_location_name = models.CharField(max_length=64)
    address = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    state_designer_num = models.CharField(max_length=100)
    contractor_lic_num = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pos_code = models.CharField(max_length=100)
