# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#TODO: please change the type of field
class Professional(models.Model):
    lic_num = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    entity_type = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=64)

class ProfessionalType(models.Model):
    professional = models.OneToOneField(Professional, primary_key=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=64)
    sub_type = models.CharField(max_length=64)



