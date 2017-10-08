# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-08 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designer',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='designer',
            name='bus_name',
            field=models.CharField(blank=True, max_length=126, null=True),
        ),
        migrations.AlterField(
            model_name='designer',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='designer',
            name='contractor_lic_num',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='designer',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='designer',
            name='email',
            field=models.CharField(blank=True, max_length=62, null=True),
        ),
        migrations.AlterField(
            model_name='designer',
            name='fax',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='designer',
            name='mobile',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='designer',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='designer',
            name='pos_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='designer',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='designer',
            name='state_designer_num',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='designer',
            name='website',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]