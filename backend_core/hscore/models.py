# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
# from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from contractors.models import Contractor
# Create your models here.

class Hscore(models.Model):

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None)
    # object_id = models.IntegerField(default=1)
    # content_object = GenericForeignKey('content_type', 'object_id')
    contractor = models.ForeignKey(
        Contractor,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='hscores',
        related_query_name='hscore'
    )
    score = models.IntegerField(null=True)
    rank = models.IntegerField(null=True)
    max = models.IntegerField(null=True)
