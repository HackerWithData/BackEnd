# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from contractors.models import Contractor
from utils import *


class User(AbstractUser):

    role = models.CharField(
        choices=ROLE_CHOICES,
        default=CONSUMER,
        max_length=16
    )

    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, null=True)


class ConsumerProfile(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(
        choices=GENDER_CHOICES,
        default=MALE,
        max_length=8
    )
    zipcode = models.CharField(
        max_length=8
    )


class ProfessionalProfile(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=64)


class ConsumerInterest(models.Model):

    consumer_profile = models.ForeignKey(ConsumerProfile, on_delete=models.CASCADE)
    interest = models.CharField(
        max_length=32
    )