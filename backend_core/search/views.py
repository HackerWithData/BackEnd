# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import render, redirect, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.urls import reverse
from django.core import serializers
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder

from professionals.utils import ARCHITECT, DESIGNER, CONTRACTOR,MEISTER
from search_helpers import (search_by_zipcode,
                            search_by_address_object_redirect_url,
                            search_by_name_or_lic)
from .utils import json_serial


# TODO: solve Type <class 'django.utils.functional.__proxy__'> not serializable
class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


#TODO: need to consider this one nothing typed?
def search_new(request):
    if request.is_ajax():
        # TODO: deal with json data
        if request.method == 'POST':
            request_json = json.loads(request.body)
            url = search_by_address_object_redirect_url(request_json)
            return HttpResponse(reverse('search_new') + '?page=1&' + url)
        else:
            raise UnexpectedRequest("Error: Unexpected request type for new search ajax request")
        return HttpResponse("Ok")
    elif request.method == 'GET':
        # TODO: set default
        if ('type' in request.GET) or ('target' in request.GET) or ('zipcode' in request.GET):
            if request.GET['type'].upper() == 'NAMEORLIC':
                if request.GET['target'] != '' or request.GET['zipcode'] !='':
                    query_set = search_by_name_or_lic(request)
                else:
                    messages.warning(request, _("please type something you want to search"))
                    return redirect(request.path)
            else:
                query_set = search_by_zipcode(request)

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

        else:
            return redirect('home_index')

        return render(request, 'search_list/search_list.html', {
            'professionals': page_query_set,
            'professionals_json': json.dumps(page_query_set.object_list, cls=LazyEncoder) if query_set else None,
            'zipcode': request.GET.get('zipcode'),
            'parameters': parameters,
        })
    else:
        messages.warning(request, _("please input something you want to search"))
        return redirect(request.path)



def search_dispatch_test(request):
    return HttpResponse('<h1>search dispatch successfully!!!</h1>')


# def search_target_type(requ
#     if request.method == 'POST':
#         target_type_search_text = request.POST['target_type_search_text']
#     else:
#         target_type_search_text = ''
#
#     contractors = Contractor.objects.filter(LicType__icontains=target_type_search_text)
#
#     return render_to_response('search_list/ajax_search_list.html', {'contractors': contractors})est):


class UnexpectedRequest(Exception):
    pass
