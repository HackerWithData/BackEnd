# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-16 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meister',
            fields=[
                ('lic_num', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('lic_name', models.CharField(max_length=255)),
                ('bus_name', models.CharField(blank=True, max_length=255)),
                ('street_address', models.CharField(blank=True, max_length=255)),
                ('county', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=63)),
                ('pos_code', models.CharField(blank=True, max_length=25)),
                ('phone', models.CharField(blank=True, max_length=25)),
            ],
        ),
    ]
