# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from forms import SearchForm


# TODO: create new search
def search_new(request, query_target, query_keywords, query_location):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():

    else:
        initial_value = {
            'query_target': 'Designer',
            'query_keywords': 'Interior Design',
            'query_location': '90024',
        }
        form = SearchForm(initial=initial_value)

    return render(request, 'search_bar/search_bar.html', {'form': form})


def search_dispatch_test(request):
    return HttpResponse('<h1>search dispatch successfully!!!</h1>')

