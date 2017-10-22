from django import forms
from django.utils.translation import pgettext, ugettext, ugettext_lazy as _

from projects.models import Project
from .models import Transaction, TransactionHistory
from utils import *


class TransactionForm(forms.Form):
    """
        Transaction form
    """

    amount = forms.FloatField(
        label=_('Amount')
    )

    create_at = forms.DateTimeField(
        label=_('Create Date')
    )

    updated_at = forms.DateTimeField(
        label=_('Update Date')
    )

    status = forms.CharField(
        choices=TRANSACTION_STATUS_CHOICES,
        default=PENDING,
        max_length=8,
        verbose_name=_('Transaction Status')
    )

    transaction_key = forms.CharField(
        max_length=32,
        verbose_name=_('Transaction ID')
    )

    def clean_amount(self):
        amount_str = self.cleaned_data['amount']
        amount = float(amount_str)
        return amount

    def save(self, request):
        clean_amount = self.cleaned_data['amount']
        clean_transaction_key = self.cleaned_data['transaction_key']
        project = Project.objects.get(id=request['project_id'])
        transaction, created = Transaction.objects.get_or_create(
            transaction_key=clean_transaction_key)
        transaction.amount = self.clean_amount
        transaction.save()

        # insert a new transaction history with pending status as soon as a transaction created
        if created:
            TransactionHistory.objects.create(transaction=transaction, status=transaction.status)


class TransactionHistoryForm(forms.Form):
    """
        Transaction history record form
    """

    create_at = forms.DateTimeField(
        label=_('Create Date')
    )

    status = forms.CharField(
        choices=TRANSACTION_STATUS_CHOICES,
        default=PENDING,
        max_length=8,
        verbose_name=_('Transaction Status')
    )
