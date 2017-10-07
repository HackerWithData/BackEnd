# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-07 02:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_type', models.CharField(choices=[('E', 'Efficiency'), ('Q', 'Quality'), ('L', 'Length')], max_length=1)),
                ('count', models.IntegerField()),
                ('total', models.IntegerField()),
                ('average', models.FloatField()),
                ('object_id', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_type', models.CharField(choices=[('E', 'Efficiency'), ('Q', 'Quality'), ('L', 'Length')], max_length=1)),
                ('rating_score', models.IntegerField()),
            ],
        ),
    ]
