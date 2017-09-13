# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation

from photos.models import Photo
from contractors.models import Contractor
from django.contrib.auth.models import User

# Create your models here.
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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    project_type = models.CharField(max_length=255)
    project_date = models.DateField()
    project_address = models.CharField(max_length=100)
    project_zipcode = models.CharField(max_length=20)
    project_cost = models.IntegerField()
    project_duration = models.IntegerField()
    comments = models.TextField()
    is_anonymous = models.BooleanField(max_length=3, choices=STATE_CHOICES, default=False)
    review_status = models.CharField(max_length=1, choices=REVIEW_STATUS, default=PENDING)
    review_date = models.DateTimeField(default=timezone.now)

    #photo
    photo = GenericRelation(Photo)