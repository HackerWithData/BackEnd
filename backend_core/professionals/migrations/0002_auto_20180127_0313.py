# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-27 03:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('professionals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datacollection',
            name='lic_num',
            field=models.CharField(max_length=63),
        ),
        migrations.AlterField(
            model_name='datacollection',
            name='professional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='professional_datacollections', related_query_name='professional_datacollection', to='professionals.Professional'),
        ),
    ]
