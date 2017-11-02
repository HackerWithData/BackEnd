# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-26 03:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20171023_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[(b'P', b'PENDING'), (b'F', b'FAILED'), (b'S', b'SUCCESS'), (b'A', b'ABORTED'), (b'C', b'CANCELED')], default=b'P', max_length=8, verbose_name='transaction status'),
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='status',
            field=models.CharField(choices=[(b'P', b'PENDING'), (b'F', b'FAILED'), (b'S', b'SUCCESS'), (b'A', b'ABORTED'), (b'C', b'CANCELED')], max_length=8, verbose_name='transaction status'),
        ),
    ]
