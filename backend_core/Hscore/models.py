# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Hscore(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey('content_type', 'object_id')
    score = models.PositiveSmallIntegerField()