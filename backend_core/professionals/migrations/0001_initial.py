# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-16 07:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('lic_num', models.CharField(max_length=63)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Professional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('owner_name', models.CharField(blank=True, max_length=63, null=True)),
                ('csp', models.CharField(max_length=127)),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(blank=True, max_length=127, null=True)),
                ('county', models.CharField(blank=True, max_length=63, null=True)),
                ('lic_status', models.CharField(blank=True, max_length=15, null=True)),
                ('phone', models.TextField(blank=True)),
                ('entity_type', models.CharField(choices=[('Corporation', 'Corporation'), ('Partnership', 'Partnership'), ('Sole Ownership', 'Sole Ownership')], max_length=31)),
                ('state', models.CharField(max_length=63)),
                ('pos_code', models.CharField(max_length=16)),
                ('uuid', models.CharField(default='0', max_length=36)),
            ],
        ),
        migrations.CreateModel(
            name='ProfessionalType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10)),
                ('subtype', models.CharField(choices=[('General Contractor', 'General Contractor'), ('Landscaping Contractor', 'Landscaping Contractor'), ('Swimming Pool Contractor', 'Swimming Pool Contractor'), ('KBR', 'Kitchen & Bath Remodeler'), ('Roofing Contractor', 'Roofing Contractor'), ('Plumbing Contractor', 'Plumbing Contractor'), ('Fencing Contractor', 'Fencing Contractor'), ('HVAC Contractor', 'HVAC Contractor'), ('Designer', 'Designer'), ('Doors, Gates and Activating Devices', 'Doors, Gates and Activating Devices'), ('Carpentry Contractor', 'Carpentry Contractor'), ('Concrete Contractor', 'Concrete Contractor'), ('Drywall Contractor', 'Drywall Contractor'), ('Electrical Contractor', 'Electrical Contractor'), ('Painting And Decorating Contractor', 'Painting And Decorating Contractor'), ('Sheet Metal Contractor', 'Sheet Metal Contractor'), ('Meister', 'Meister'), ('Architect', 'Architect')], max_length=127)),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='professional_types', related_query_name='professional_type', to='professionals.Professional')),
            ],
        ),
        migrations.AddField(
            model_name='datacollection',
            name='professional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='professional_datacollections', related_query_name='professional_datacollection', to='professionals.Professional'),
        ),
    ]
