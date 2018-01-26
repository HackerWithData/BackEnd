# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class DataSource(models.Model):
    class Meta:
        abstract = True

    lic_num = models.CharField(max_length=127)
    lic_type = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    name = models.CharField(max_length=63)
    lic_state = models.CharField(max_length=15)
    lic_board = models.CharField(max_length=255)
    lic_status = models.CharField(max_length=30)
    address = models.CharField(max_length=255)


class DataSourceElpaso(DataSource):
    state_lic_num = models.CharField(max_length=127)
    name2 = models.CharField(max_length=63)
    phone = models.TextField()
    email = models.EmailField()
    lic_issue_date = models.DateField()
    lic_expire_date = models.DateField()
    bus_expire_date = models.DateField()
    insur_company = models.CharField(max_length=63)
    insur_policy = models.TextField()
