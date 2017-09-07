# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
# # from forms import BaseSearchForm
# from forms import TargetTypeSearchForm
from contractors.models import Contractor


def search_new(request):
    # if request.method == 'POST':
    #     form = SearchForm(request.POST)
    #     if form.is_valid():
    #         pass
    #
    # else:
    #     initial_value = {
    #         'query_target': 'Designer',
    #         'query_keywords': 'Interior Design',
    #         'query_location': '90024',
    #     }
    #     form = SearchForm(initial=initial_value)
    if request.method == 'GET':
        # TODO: set default value
        target = request.GET['target']
        # keywords = request.GET['keywords']
        zipcode = request.GET['zipcode']
        query_set = Contractor.objects.filter(PosCode=zipcode).filter(LicType__icontains=target)
    else:
        return redirect('home_index')
    return render(request, 'search_list/search_list.html', {'contractors': query_set})

#
# def search(request):
#     # form = BaseSearchForm(request.GET)
#     form = TargetTypeSearchForm(request.GET)
#     results = form.search()
#     return render_to_response('search_bar.html', {'results': results})
#
#
def search_dispatch_test(request):
    return HttpResponse('<h1>search dispatch successfully!!!</h1>')

# def search_target_type(request):
#     if request.method == 'POST':
#         target_type_search_text = request.POST['target_type_search_text']
#     else:
#         target_type_search_text = ''
#
#     contractors = Contractor.objects.filter(LicType__icontains=target_type_search_text)
#
#     return render_to_response('search_list/ajax_search_list.html', {'contractors': contractors})
