# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-09 02:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0004_auto_20171008_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bondcompany',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bondcompany',
            name='county',
            field=models.CharField(blank=True, max_length=63, null=True),
        ),
        migrations.AlterField(
            model_name='bondcompany',
            name='pos_code',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='bondcompany',
            name='state',
            field=models.CharField(blank=True, max_length=63, null=True),
        ),
        migrations.AlterField(
            model_name='bondcompany',
            name='surety_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='bondhistory',
            name='bond_cancellation_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bondhistory',
            name='bond_effective_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bondhistory',
            name='contractor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contractors.Contractor'),
        ),
        migrations.AlterField(
            model_name='bondhistory',
            name='surety_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='contractors.BondCompany'),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='csp',
            field=models.CharField(blank=True, max_length=63),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='dba',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='entity',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='lic_status',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='phone',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='pos_code',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='state',
            field=models.CharField(max_length=63),
        ),
        migrations.AlterField(
            model_name='inssurancecompany',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='inssurancecompany',
            name='county',
            field=models.CharField(max_length=63),
        ),
        migrations.AlterField(
            model_name='inssurancecompany',
            name='insur_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='inssurancecompany',
            name='pos_code',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='inssurancecompany',
            name='state',
            field=models.CharField(max_length=63),
        ),
        migrations.AlterField(
            model_name='licenserelation',
            name='contractor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='contractor', to='contractors.Contractor'),
        ),
        migrations.AlterField(
            model_name='licenserelation',
            name='name',
            field=models.CharField(max_length=63),
        ),
        migrations.AlterField(
            model_name='licenserelation',
            name='related_contractor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='related_contractor', to='contractors.Contractor'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='contractor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contractors.Contractor'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='lic_type',
            field=models.CharField(max_length=63),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='name',
            field=models.CharField(max_length=63),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='title',
            field=models.CharField(max_length=63),
        ),
        migrations.AlterField(
            model_name='workercompensationhistory',
            name='contractor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contractors.Contractor'),
        ),
        migrations.AlterField(
            model_name='workercompensationhistory',
            name='insur_cancellation_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workercompensationhistory',
            name='insur_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='contractors.InssuranceCompany'),
        ),
        migrations.AlterField(
            model_name='workercompensationhistory',
            name='insur_effective_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]