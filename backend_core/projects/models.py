# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as __


# Create your models here.
# TODO: Consider cache ?? Interesting!
class Project(models.Model):
    PENDING = 'P'
    ACCEPTED = 'A'
    REJECTED = 'R'
    ONGOING = "O"
    DONE = "D"
    PROJECT_STATUS = (
        (PENDING, __('PENDING')),
        (ACCEPTED, __('ACCEPTED')),
        (ONGOING, __('ONGOING')),
        (REJECTED, __('REJECTED')),
        (DONE, __('DONE')),
    )

    REMODEL = "R"
    NEWBUILT = "N"
    PROJECT_TYPE = (
        ("",'-----'),
        (REMODEL, __('REMODEL')),
        (NEWBUILT, __("NEW BUILT HOUSE")),
    )
    project_id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    bus_name = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # user.id how to get user id
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    # Project Type choice field
    project_type = models.CharField(max_length=5, choices=PROJECT_TYPE, default=None, null=False, blank=True)
    street_address = models.TextField()
    street_address2 = models.TextField()
    county = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=10)
    #country = models.CharField(max_length=255)
    project_cost = models.IntegerField(default=0)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    project_description = models.TextField()
    project_status = models.CharField(max_length=1, choices=PROJECT_STATUS, default=ONGOING)
    project_action = models.TextField(null=True, blank=True)
    # Project_Action =

    class Meta:
        unique_together = ('project_id', 'content_type', 'object_id', 'user')


class ProjectAttachment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    attachment_type = models.CharField(max_length=100)
    project_attachment = models.FileField(upload_to='project_attachment/%Y/%m/%d')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)


class ProjectPhoto(models.Model):
    project_photo = models.ImageField(upload_to='projects/photos/%Y/%m/%d')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
