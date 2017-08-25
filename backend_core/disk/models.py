# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

"""
class image(models.Model):
    image = models.ImageField(upload_to="phtots/%Y/%m/%d", blank=True, null=True)
"""

class UserFile(models.Model):
    userName = models.CharField(max_length=30)
    uploadFile = models.FileField(upload_to='disk/upload')

    def __str__(self):
        return self.userName
