# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _

from users.models import CONSUMER, ROLE_CHOICES
from professionals.models import Professional

# Create your models here.
# TODO: Consider cache ?? Interesting!

WAITING = "W"
PAID_TO_HOOME = "PTH"
PAID_TO_PROFESSIONAL = "PTP"

PAYMENT_REQUEST = 'M'

WAITING_ACTION = "Contractor is waiting for the payment"

PENDING = 'P'
ACCEPTED = 'A'
REJECTED = 'R'
ONGOING = "O"
DONE = "D"

MILESTONE_STATUS = (
    (WAITING, _("Waiting")),
    (PAID_TO_HOOME, _("Paid to Hoome")),
    (PAID_TO_PROFESSIONAL, _("Paid to Professional")),
    (DONE, _("Done")),
    (PAYMENT_REQUEST, _("Payment Request")),
)

PROJECT_STATUS = (
    (PENDING, _('PENDING')),
    (ACCEPTED, _('ACCEPTED')),
    (ONGOING, _('ONGOING')),
    (REJECTED, _('REJECTED')),
    (DONE, _('DONE')),
)

REMODEL = "R"
NEW_BUILT = "N"
PROJECT_TYPE = ((REMODEL, _('REMODEL')),
    (NEW_BUILT, _("NEW BUILT HOUSE")),
)


class Project(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    bus_name = models.CharField(max_length=255, blank=True)
    professional = models.ForeignKey(Professional, on_delete=models.DO_NOTHING, null=True)
    # user.id how to get user id
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    # Project Type choice field
    project_type = models.CharField(max_length=5, choices=PROJECT_TYPE, default=REMODEL, null=False, blank=True)
    street_address = models.TextField(blank=True)
    street_address2 = models.TextField(blank=True)
    county = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=64, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    # country = models.CharField(max_length=255)
    project_cost = models.IntegerField(default=0)
    contract_price = models.IntegerField(default=0)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)
    project_description = models.TextField(blank=True)
    project_status = models.CharField(max_length=1, default=WAITING)  # choices=PROJECT_STATUS,
    project_action = models.TextField(blank=True)
    uuid = models.CharField(max_length=36, default='0')  # choices=PROJECT_STATUS,
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(default=CONSUMER, choices=ROLE_CHOICES, max_length=16)

    class Meta:
        unique_together = ('project_id', 'professional', 'user')


class ProjectAttachment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    attachment_type = models.CharField(max_length=100)
    project_attachment = models.FileField(upload_to='projects/attachments/%Y/%m/%d')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)


class ProjectPhoto(models.Model):
    project_photo = models.ImageField(upload_to='projects/photos/%Y/%m/%d')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)


class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=63, choices=MILESTONE_STATUS, default=WAITING)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=36, default='0')
