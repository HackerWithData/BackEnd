# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-17 01:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professionals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professional',
            name='type',
            field=models.CharField(choices=[(b'CONTRACTOR', 'Contractor'), (b'ARCHITECT', 'Architect'), (b'DESIGNER', 'Designer'), (b'MEISTER', 'Meister')], max_length=10),
        ),
    ]
