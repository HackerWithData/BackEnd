# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
# # from forms import BaseSearchForm
# from forms import TargetTypeSearchForm
from contractors.models import Contractor


def search_new(request):
    if request.method == 'GET':
        # TODO: set default value
        target = request.GET['target']
        # keywords = request.GET['keywords']
        zipcode = request.GET['zipcode']
        query_set = Contractor.objects.filter(PosCode=zipcode).filter(LicType__icontains=target)

        # TODO: set customized item number per page, default = 10
        # pagination logic
        paginator = Paginator(query_set, 10)
        page = request.GET.get('page')
        try:
            page_query_set = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_query_set = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_query_set = paginator.page(paginator.num_pages)

        get_copy = request.GET.copy()
        parameters = get_copy.pop('page', True) and get_copy.urlencode()

        print parameters
        # context['constractors'] =
        # context = {
        #     'contractors': page_query_set,
        #     'parameters': parameters
        # }
    else:
        return redirect('home_index')
    return render(request, 'search_list/search_list.html', {
        'contractors': page_query_set,
        'parameters': parameters
    })


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
