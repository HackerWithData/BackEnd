# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-22 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectattachment',
            name='project_attachment',
            field=models.FileField(upload_to='project_attachment/%Y/%m/%d'),
        ),
    ]
