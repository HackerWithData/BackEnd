# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-16 01:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasources', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datasourceelapso',
            name='bussiness_lic_num',
        ),
    ]
