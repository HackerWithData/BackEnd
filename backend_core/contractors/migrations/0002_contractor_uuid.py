# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-02 22:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractor',
            name='uuid',
            field=models.CharField(default='0', max_length=36),
        ),
    ]