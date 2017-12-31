# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from hscore.models import Hscore
from utils import *


class Professional(models.Model):
    lic_num = models.CharField(max_length=63)
    name = models.CharField(max_length=255, blank=True, null=True)
    entity_type = models.CharField(
        max_length=63,
        choices=ENTITY_CHOICES, blank=True, null=True
    )
    type = models.CharField(
        max_length=63,
        choices=PROFESSIONAL_CHOICES, blank=True, null=True
    )
    state = models.CharField(max_length=63, blank=True, null=True)
    lic_type = models.TextField(default='NO LIC TYPE', blank=True, null=True)
    # TODO: need to change the name to pos_code later
    county = models.CharField(max_length=63, blank=True, null=True)
    postal_code = models.CharField(max_length=63, blank=True, null=True)


class ProfessionalType(models.Model):
    professional = models.ForeignKey(
        Professional,
        on_delete=models.DO_NOTHING,
        related_name='professional_types',
        related_query_name='professional_type'
    )
    type = models.CharField(max_length=10)
    subtype = models.CharField(
        max_length=255,
        choices=PROFESSIONAL_SUBTYPE_CHOICES
    )
