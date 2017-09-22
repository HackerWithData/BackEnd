# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from utils import PROFESSIONAL_TYPE_CHOICES, ARCHITECT, DESIGNER, CONTRACTOR


#TODO: please change the type of field
class Professional(models.Model):
    lic_num = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    entity_type = models.CharField(max_length=64)
    type = models.CharField(
        max_length=64,
        choices=PROFESSIONAL_TYPE_CHOICES
    )
    state = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=64)


class ProfessionalType(models.Model):
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name='professional_types',
        related_query_name='professional_type'
    )
    type = models.CharField(max_length=64)
    sub_type = models.CharField(max_length=64)
