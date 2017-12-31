# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.


class Meister(models.Model):
    lic_id = models.BigAutoField(primary_key=True, unique=True)
    lic_num = models.IntegerField(null=True)
    lic_name = models.CharField(max_length=255)
    bus_name = models.CharField(max_length=255, blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    county = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=63, blank=True)
    pos_code = models.CharField(max_length=25, blank=True)
    phone = models.CharField(max_length=25, blank=True)

    def __iter__(self):
        return self.__dict__.iteritems()