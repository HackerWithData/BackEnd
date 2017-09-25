# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from utils import *


class Professional(models.Model):
    lic_num = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    entity_type = models.CharField(
        max_length=64,
        choices=ENTITY_CHOICES
    )
    type = models.CharField(
        max_length=64,
        choices=PROFESSIONAL_CHOICES
    )
    state = models.CharField(max_length=64)
    #TODO:ADD a lic type
    lic_type = models.CharField(max_length=256)
    postal_code = models.CharField(max_length=64)


class ProfessionalType(models.Model):
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name='professional_types',
        related_query_name='professional_type'
    )
    type = models.CharField(max_length=128)
    subtype = models.CharField(
        max_length=128,
        choices=PROFESSIONAL_SUBTYPE_CHOICES
    )
