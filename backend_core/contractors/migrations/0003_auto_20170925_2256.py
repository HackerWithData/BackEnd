# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-25 22:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0002_auto_20170925_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractor',
            name='lic_expire_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='lic_issue_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
