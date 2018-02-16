# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from datetime import datetime

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from projects.utils import get_user_projects
from .forms import TransactionForm, TransactionHistoryForm
from .utils import (
    get_transactions,
    get_or_create_transaction,
    generate_transaction_uuid,
    create_transaction_history,
)
from .models import SUCCESS
from projects.models import PAID_TO_HOOME
from projects.utils import (
    get_milestone,
    get_project,
    update_milestone,
)

# Create your views here.
# TODO: Simplify this part
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
        template_name = 'transaction/transactions.html'
        transactions = get_transactions(request.user)
        info_dict = {'transactions': transactions}
        return render(request, template_name, {'info_dict': info_dict})

    def post(self, request, *args, **kwargs):
        """
            create a new transaction
            :param request:
            :param args:
            :param kwargs:
            :return:
        """
        received_json_data = json.loads(request.body)
        project = get_project(uuid_=received_json_data['project_uuid'])
        milestone = get_milestone(uuid=received_json_data['milestone_uuid'])
        # TODO: should change here because should save to the model at the time. change get or create to get and models()
        transaction, created = get_or_create_transaction(
            **{
                'project': project,
                'user': project.user,
                'milestone': milestone,
                'professional': project.professional,
                'transaction_key': received_json_data['transaction_key']
        })

        # TODO: consider wheter ignore to use get_or_create since it will query 2 times. we sill need to change Person object after created.
        # TODO: better to redesign here
        if created:
            if received_json_data['amount'] == '':
                pass
            else:
                transaction.amount = float(received_json_data['amount'])
            transaction.created_at = datetime.utcfromtimestamp(received_json_data['created_at'])
            transaction.uuid = generate_transaction_uuid()

        transaction.status = received_json_data['status'].upper()[0]
        transaction.save()
        # TODO: we can remove this conditional statement probably
        if transaction.status == SUCCESS:
            update_milestone(milestone=milestone, **{'status': PAID_TO_HOOME})
        # insert a new transaction history with pending status as soon as a transaction created
        create_transaction_history(transaction=transaction)
        # TODO: should refresh the page. or refresh some part of html
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


@login_required
def project_checkout(request):
    template_name = 'transaction/checkout.html'

    # TODO: Add status filter
    projects = get_user_projects(user=request.user)
    info_dict = {'projects': projects}
    if request.method == 'GET':
        return render(request, template_name, {'info_dict': info_dict})
    elif request.method == 'POST':
        # try:
        #     project = Project.objects.get(project=request.POST.get['project_id'])
        #     return render(request, redirect_template_name, {'info_dict': info_dict})
        # except:
        #     messages.success(request, _("Your Profile updated."))
        #     return render(request, template_name, {'info_dict': info_dict})
        url = '/checkout/' + request.POST.get('project_uuid')
        return redirect(url)


#TODO: need to take care project_uuid here
def project_pay(request, project_uuid):
    template_name = 'transaction/payment.html'
    projects = get_project(uuid_=project_uuid)
    info_dict = {'project': projects}
    return render(request, template_name, {'info_dict': info_dict})
