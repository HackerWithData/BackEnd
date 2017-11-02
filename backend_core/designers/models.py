# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# TODO: please change the type of field
# TODO: need to redesign the architecture of designer
class Designer(models.Model):
    lic_num = models.IntegerField(primary_key=True, unique=True)
    lic_type = models.CharField(max_length=10)
    lic_name = models.CharField(max_length=63)
    bus_name = models.CharField(max_length=255, blank=True, null=True)
    office_location_name = models.CharField(max_length=62)
    website = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    state_designer_num = models.CharField(max_length=15, blank=True, null=True)
    contractor_lic_num = models.CharField(max_length=15, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=63, blank=True, null=True)
    state = models.CharField(max_length=63, blank=True, null=True)
    pos_code = models.CharField(max_length=25, blank=True, null=True)
    country = models.CharField(max_length=63, blank=True, null=True)

    def __iter__(self):
        return self.__dict__.iteritems()

