# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-30 02:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_transaction_transaction_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_uuid',
            field=models.CharField(default='0', max_length=36),
        ),
    ]