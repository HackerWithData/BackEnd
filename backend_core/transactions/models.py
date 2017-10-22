# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from projects.models import Project
from .utils import *


# Create your models here.
class Transaction(models.Model):
    """
        transaction model
    """
    amount = models.FloatField(
        verbose_name=_('amount')
    )

    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated at')
    )

    status = models.CharField(
        choices=TRANSACTION_STATUS_CHOICES,
        default=PENDING,
        max_length=8,
        verbose_name=_('transaction status')
    )

    transaction_key = models.CharField(
        max_length=32,
        unique=True
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.DO_NOTHING,
        related_name='transactions',
        related_query_name='transaction'
    )


class TransactionHistory(models.Model):
    """
        transaction histroy record model
    """
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.DO_NOTHING,
        related_name='transaction_histories',
        related_query_name='transaction_history'
    )

    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )

    status = models.CharField(
        choices=TRANSACTION_STATUS_CHOICES,
        max_length=8,
        verbose_name=_('transaction status')
    )
