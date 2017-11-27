# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from tinymce import models as tinymce_models

# Create your models here.


class Overview(models.Model):
    overview = tinymce_models.HTMLField()
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')