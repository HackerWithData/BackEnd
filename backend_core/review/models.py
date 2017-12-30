# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from photos.models import Photo
from projects.utils import (PROJECT_TYPE)


# Create your models here.

#TODO: need to rewrite this part. Way too dumb
class Review(models.Model):
    PENDING = 'P'
    ACCEPTED = 'A'
    REJECTED = 'R'
    REVIEW_STATUS = (
        (PENDING, 'PENDING'),
        (ACCEPTED, 'ACCEPTED'),
        (REJECTED, 'REJECTED'),
    )

    STATE_CHOICES = (
        (True, u"Yes"),
        (False, u"No"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    project_type = models.CharField(max_length=255, choices=PROJECT_TYPE, )
    project_date = models.DateField()
    street_address = models.TextField()
    street_address2 = models.TextField()
    county = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=10)
    project_zipcode = models.CharField(max_length=20)
    project_cost = models.IntegerField()
    project_duration = models.IntegerField()
    comments = models.TextField()
    is_anonymous = models.BooleanField(max_length=3, choices=STATE_CHOICES, default=False)
    review_status = models.CharField(max_length=1, choices=REVIEW_STATUS, default=ACCEPTED)
    review_date = models.DateTimeField(default=timezone.now)
    # photo
    photo = GenericRelation(Photo)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey('content_type', 'object_id')
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=255)
