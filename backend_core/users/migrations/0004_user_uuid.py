# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-06 02:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20171203_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='uuid',
            field=models.CharField(default=0, max_length=36),
        ),
    ]
