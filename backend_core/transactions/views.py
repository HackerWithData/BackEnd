# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from .forms import TransactionForm, TransactionHistoryForm
from .utils import *
from projects.models import Project
from .models import Transaction, TransactionHistory
import json


# Create your views here.
@method_decorator(login_required, name='dispatch')
class TransactionsView(View):
    form_class = TransactionForm
    initial = {
        'amount': 0,
        'status': '',
        'create_at': '',
        'updated_at': '',
        'transaction_key': ''
    }

    def get(self, request, *args, **kwargs):
        """
            show transaction list
            :param request:
            :param args:
            :param kwargs:
            :return:
        """

        return Http404

    def post(self, request, *args, **kwargs):
        """
            create a new transaction
            :param request:
            :param args:
            :param kwargs:
            :return:
        """
        received_json_data = json.loads(request.body)
        print(received_json_data)
        if 'status' in received_json_data:
            project = Project.objects.get(project_id=int(received_json_data['project_id']))
            transaction = Transaction.objects.get(project=project,
                                                  transaction_key=received_json_data['transaction_key'])
            transaction.amount = float(received_json_data['amount'])
            transaction.status = received_json_data['status'].upper()[0]
            transaction.save()
            transaction_history = TransactionHistory.objects.get(transaction=transaction)
            transaction_history.status = transaction.status
            transaction_history.save()
        else:
            # print(received_json_data)
            # TODO: need to change this part


            project = Project.objects.get(project_id=int(received_json_data['project_id']))
            transaction, created = Transaction.objects.get_or_create(project=project,
                                                     transaction_key=received_json_data['transaction_key'])
            if created:
                if received_json_data['amount'] == '':
                    pass
                else:
                    transaction.amount = float(received_json_data['amount'])
                transaction.created_at = datetime.utcfromtimestamp(received_json_data['created_at'])
                transaction.save()

                # insert a new transaction history with pending status as soon as a transaction created
                transaction_history = TransactionHistory.objects.create(transaction=transaction, status=transaction.status)
                transaction_history.save()
            else:
                pass
            # #fields
        return HttpResponse(status=204)


@method_decorator(login_required, name='dispatch')
class TransactionView(View):
    form_class = TransactionForm
    initial = {
        'amount': 0,
        'status': '',
        'create_at': '',
        'updated_at': '',
        'transaction_key': ''
    }

    def get(self, request, *args, **kwargs):
        """
            show specific transaction
            :param request:
            :param args:
            :param kwargs:
            :return:
        """
        pass

    def post(self, request, *args, **kwargs):
        """
            not allowed method
            :param request:
            :param args:
            :param kwargs:
            :return:
        """
        return HttpResponseNotAllowed


@method_decorator(login_required, name='dispatch')
class TransactionHistoryView(View):
    form_class = TransactionHistoryForm
    initial = {
        'status': '',
        'create_at': '',
    }

    def get(self, request, *args, **kwargs):
        """
            how specific transaction history
            :param request:
            :param args:
            :param kwargs:
            :return:
        """
        # TODO: show the transaction detail through GET request
        pass

    def post(self, request, *args, **kwargs):
        """
            not allowed method
            :param request:
            :param args:
            :param kwargs:
            :return:
        """
        return HttpResponseNotAllowed


@method_decorator(login_required, name='dispatch')
class TransactionHistoriesView(View):
    form_class = TransactionHistoryForm
    initial = {
        'status': '',
        'create_at': '',
    }

    def get(self, request, *args, **kwargs):
        """
            show transaction history list
            :param request:
            :param args:
            :param kwargs:
            :return:
        """
        # TODO: show the transaction history list through GET request
        pass

    def post(self, request, *args, **kwargs):
        """
            create a new transaction history
            :param request:
            :param args:
            :param kwargs:
            :return:
        """
        pass
