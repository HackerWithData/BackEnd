# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View


# Create your views here.
@method_decorator(login_required, name='dispatch')
class TransactionView(View):

    form_class = TransactionForm
    template_name = ''
    initial = {}

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # TODO: show the transaction detail through GET request
        # form = self.form_class(initial=self.initial)
        # return render(request, self.template_name, {'form': form})
        return Http404

    def post(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(request)

        return HttpResponse(status=204)
