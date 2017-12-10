# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .utils import (PROJECT_TYPE, MILESTONE_STATUS, REMODEL, WAITING)
from users.utils import CONSUMER, ROLE_CHOICES


# Create your models here.
# TODO: Consider cache ?? Interesting!

class Project(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    bus_name = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    # user.id how to get user id
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    # Project Type choice field
    project_type = models.CharField(max_length=5, choices=PROJECT_TYPE, default=REMODEL, null=False, blank=True)
    street_address = models.TextField()
    street_address2 = models.TextField()
    county = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=10)
    # country = models.CharField(max_length=255)
    project_cost = models.IntegerField(default=0)
    contract_price = models.IntegerField(default=0)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)
    project_description = models.TextField()
    project_status = models.CharField(max_length=1, default=WAITING)  # choices=PROJECT_STATUS,
    project_action = models.TextField(null=True, blank=True)
    uuid = models.CharField(max_length=36, default='0')  # choices=PROJECT_STATUS,
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(default=CONSUMER, choices=ROLE_CHOICES, max_length=16)

    class Meta:
        unique_together = ('project_id', 'content_type', 'object_id', 'user')


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
