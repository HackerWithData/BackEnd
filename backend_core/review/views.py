# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Create your views here.
# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect
from forms import ReviewForm
from models import Review
# Create your views here.

def submit_review(request,contracotr_id):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            rv = Review()
            #if request.user.is_authenticated:
            #    rv.first_name = request.user.first_name
            #    rv.last_name = request.user.last_name

            #rv.first_name = rv.cleaned_data['first_name']
            #rv.last_name = rv.clean_date['last_name']
            #rv.uploadFile = rv.cleaned_data['uploadFile']
            rv.save()
            return render(request,'disk/uploadsuccess.html') #redirect('/')#
    else:

        if request.user.is_authenticated:
            review_form = ReviewForm(initial={'first_name': request.user.first_name,'last_name': request.user.last_name})
        else:
            review_form = ReviewForm()
        return render(request, 'review/submit.html',{'review_form':review_form})


