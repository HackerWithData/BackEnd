# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 02:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='object_id',
        ),
    ]
