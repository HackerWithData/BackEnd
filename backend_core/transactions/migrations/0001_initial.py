# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-02 01:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0, verbose_name='amount')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('status', models.CharField(choices=[(b'P', b'PENDING'), (b'F', b'FAILED'), (b'S', b'SUCCESS'), (b'A', b'ABORTED'), (b'C', b'CANCELED')], default=b'P', max_length=8, verbose_name='transaction status')),
                ('transaction_key', models.CharField(max_length=32, unique=True)),
                ('object_id', models.PositiveIntegerField()),
                ('transaction_uuid', models.CharField(default='0', max_length=36)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contenttypes.ContentType')),
                ('milestone', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transactions', related_query_name='transaction', to='projects.Milestone')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transactions', related_query_name='transaction', to='projects.Project', verbose_name='project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('status', models.CharField(choices=[(b'P', b'PENDING'), (b'F', b'FAILED'), (b'S', b'SUCCESS'), (b'A', b'ABORTED'), (b'C', b'CANCELED')], max_length=8, verbose_name='transaction status')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transaction_histories', related_query_name='transaction_history', to='transactions.Transaction')),
            ],
        ),
    ]
