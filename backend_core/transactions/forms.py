from django import forms
from django.utils.translation import pgettext, ugettext, ugettext_lazy as _


from utils import *


class TransactionForm(forms.Form):
    """
        Transaction form
    """

    amount = forms.FloatField(
        label=_('Amount')
    )

    status = forms.CharField(
        max_length=8,
        label=_('Transaction Status')
    )

    transaction_key = forms.CharField(
        max_length=32,
        label=_('Transaction ID')
    )
    project_id = forms.IntegerField()





class TransactionHistoryForm(forms.Form):
    """
        Transaction history record form
    """

    create_at = forms.DateTimeField(
        label=_('Created Date')
    )

    status = forms.CharField(
        max_length=8,
        label=_('Transaction Status')
    )
