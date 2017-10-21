# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-19 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professionals', '0003_auto_20171009_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professionaltype',
            name='subtype',
            field=models.CharField(choices=[(b'General Contractor', 'General Contractor'), (b'Landscaping Contractor', 'Landscaping Contractor'), (b'Swimming Pool Contractor', 'Swimming Pool Contractor'), (b'KBR', 'Kitchen & Bath Remodeler'), (b'Roofing Contractor', 'Roofing Contractor'), (b'Plumbing Contractor', 'Plumbing Contractor'), (b'Fencing Contractor', 'Fencing Contractor'), (b'HVAC Contractor', 'HVAC Contractor'), (b'Designer', 'Designer'), (b'Doors, Gates and Activating Devices', 'Doors, Gates and Activating Devices'), (b'Carpentry Contractor', 'Carpentry Contractor'), (b'Concrete Contractor', 'Concrete Contractor'), (b'Drywall Contractor', 'Drywall Contractor'), (b'Electrical Contractor', 'Electrical Contractor'), (b'Painting And Decorating Contractor', 'Painting And Decorating Contractor'), (b'Sheet Metal Contractor', 'Sheet Metal Contractor')], max_length=255),
        ),
    ]