# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from review.models import Review
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.


class UserRating(models.Model):
    EFFICIENCY = 'E'
    QUALITY = 'Q'
    LENGTH = 'L'
    RATING_TYPES = (
        (EFFICIENCY, 'Efficiency'),
        (QUALITY, 'Quality'),
        (LENGTH, 'Length'),
    )

    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    rating_type = models.CharField(max_length=1, choices=RATING_TYPES)
    rating_score = models.IntegerField()


class Rating(models.Model):
    EFFICIENCY = 'E'
    QUALITY = 'Q'
    LENGTH = 'L'
    RATING_TYPES = (
        (EFFICIENCY, 'Efficiency'),
        (QUALITY, 'Quality'),
        (LENGTH, 'Length'),
    )
    rating_type = models.CharField(max_length=1, choices=RATING_TYPES)
    count = models.IntegerField()
    total = models.IntegerField()
    average = models.FloatField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey('content_type', 'object_id')
