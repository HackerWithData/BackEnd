# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-09 23:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20171209_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectattachment',
            name='project_attachment',
            field=models.FileField(upload_to='projects/attachments/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='projectphoto',
            name='project_photo',
            field=models.ImageField(upload_to='projects/photos/%Y/%m/%d'),
        ),
    ]
