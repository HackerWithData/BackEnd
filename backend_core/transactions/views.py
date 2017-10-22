# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from .forms import TransactionForm, TransactionHistoryForm
from .utils import *


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
        form = self.form_class(self.initial)
        if form.is_valid():
            form.save(request.POST)

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
