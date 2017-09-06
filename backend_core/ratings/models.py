# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from contractors.models import Contractor
from review.models import Review
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
    rating_score = models. IntegerField()


class Rating(models.Model):
    EFFICIENCY = 'E'
    QUALITY = 'Q'
    LENGTH = 'L'
    RATING_TYPES = (
        (EFFICIENCY, 'Efficiency'),
        (QUALITY, 'Quality'),
        (LENGTH, 'Length'),
    )
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    rating_type = models.CharField(max_length=1, choices=RATING_TYPES)
    count = models.IntegerField()
    total = models.IntegerField()
    average = models.FloatField()

