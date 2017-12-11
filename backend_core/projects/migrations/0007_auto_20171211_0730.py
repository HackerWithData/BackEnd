# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-11 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20171209_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='bus_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='project',
            name='county',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='project',
            name='first_name',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='project',
            name='last_name',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_action',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='state',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='project',
            name='street_address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='street_address2',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='zipcode',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
