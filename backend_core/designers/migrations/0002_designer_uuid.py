# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-02 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='designer',
            name='uuid',
            field=models.CharField(default='0', max_length=36)
        ),
    ]
