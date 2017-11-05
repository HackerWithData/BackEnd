# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-05 00:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_type', models.CharField(max_length=255)),
                ('project_date', models.DateField()),
                ('project_address', models.CharField(max_length=100)),
                ('project_zipcode', models.CharField(max_length=20)),
                ('project_cost', models.IntegerField()),
                ('project_duration', models.IntegerField()),
                ('comments', models.TextField()),
                ('is_anonymous', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, max_length=3)),
                ('review_status', models.CharField(choices=[('P', 'PENDING'), ('A', 'ACCEPTED'), ('R', 'REJECTED')], default='A', max_length=1)),
                ('review_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('object_id', models.PositiveIntegerField(default=1)),
                ('content_type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
    ]
