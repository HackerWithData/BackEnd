# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from tinymce import models as tinymce_models

from professionals.models import Professional

# Create your models here.


class Overview(models.Model):
    overview = tinymce_models.HTMLField()
    professional = models.ForeignKey(Professional, on_delete=models.DO_NOTHING, null=True)