# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from professionals.models import Professional
from utils import *


class User(AbstractUser):

    role = models.CharField(
        choices=ROLE_CHOICES,
        default=CONSUMER,
        max_length=16
    )

    hoome_id = models.CharField(max_length=32)


class ConsumerProfile(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='consumer_profiles',
        related_query_name='consumer_profile'
    )
    gender = models.CharField(
        choices=GENDER_CHOICES,
        default=MALE,
        max_length=8
    )
    zipcode = models.CharField(
        max_length=8
    )


class ProfessionalProfile(models.Model):

    professional = models.ForeignKey(
        Professional,
        related_name='professional_profiles',
        related_query_name='professional_profile'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='professional_profiles',
        related_query_name='professional_profile'
    )

    class Meta:
        unique_together = ('user','professional')


class ConsumerInterest(models.Model):

    consumer_profile = models.ForeignKey(
        ConsumerProfile,
        on_delete=models.DO_NOTHING,
        related_name='consumer_interests',
        related_query_name='consumer_interest'
    )
    interest = models.CharField(
        max_length=32
    )


class HoomeId(models.Model):
    hoome_id = models.CharField(max_length=32)
    status = models.CharField(max_length=8, choices=ID_STATUS)
