# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-23 06:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_remove_project_country'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='cost',
            new_name='project_cost',
        ),
    ]