# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# TODO: please change the type of field
# TODO: need to redesign the architecture of designer
class Designer(models.Model):
    lic_num = models.IntegerField(primary_key=True, unique=True)
    lic_type = models.CharField(max_length=62)
    lic_name = models.CharField(max_length=100)
    bus_name = models.CharField(max_length=126, blank=True)
    office_location_name = models.CharField(max_length=62)
    website = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    fax = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=62, blank=True)
    address = models.CharField(max_length=255, blank=True)
    state_designer_num = models.CharField(max_length=100, blank=True)
    contractor_lic_num = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pos_code = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)

