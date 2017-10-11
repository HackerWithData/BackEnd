# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from hscore.models import Hscore
from utils import *


class Professional(models.Model):
    lic_num = models.CharField(max_length=25)
    name = models.CharField(max_length=255)
    entity_type = models.CharField(
        max_length=63,
        choices=ENTITY_CHOICES
    )
    type = models.CharField(
        max_length=10,
        choices=PROFESSIONAL_CHOICES
    )
    state = models.CharField(max_length=63)
    lic_type = models.TextField(default='NO LIC TYPE')
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
