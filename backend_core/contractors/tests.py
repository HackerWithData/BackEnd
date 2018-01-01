from __future__ import unicode_literals
import datetime
import json
from copy import deepcopy

from django.test import TestCase, RequestFactory, override_settings
from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.contrib.messages.storage.fallback import FallbackStorage
from django.forms import ValidationError

from projects.models import PROJECT_TYPE
from .models import Contractor
from .views import ContractorDetail
from users.models import User
from review.models import Review


class ContractorTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.url = '/contractor/1'
        Contractor.objects.create(
            lic_num=1,
            lic_expire_date=datetime.date(2100, 12, 31),
            lic_issue_date=datetime.date(2000, 1, 1),
            lic_status='Active',
            lic_type='CONTRACTOR',
        )
        self.user = User.objects.create_user(
            username='zzz',
            password='123',
            email='zzz@gx.coq',
        )
        self.view = ContractorDetail.as_view()
        self.form_data = {
            'review': True,
            'comments': 'dadada',
            'first_name': 'qqq',
            'last_name': 'www',
            'project_date': datetime.date.today(),
            'project_type': 'R',
            'project_cost': 12345,
            'project_duration': 123,
            'email': 'asxc@az.aa',
            'street_address': '23sf12',
            'street_address2': 'qwezxc',
            'county': 'azxc',
            'state': 'qq',
            'zipcode': 12345,
            'is_anonymous': False,

            'user_rating_form': True,
            'e_rating': 7,
            'q_rating': 8,
            'l_rating': 9,
        }

    def test_get_anonymous(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        response = self.view(request=request, **{'o_id': 1})
        self.assertEqual(response.status_code, 200)

    def test_get_authencateduser(self):
        request = self.factory.get(self.url)
        request.user = self.user
        response = self.view(request=request, **{'o_id': 1})
        self.assertEqual(response.status_code, 200)

    def test_get_not_exist_id(self):
        request = self.factory.get(self.url)
        request.user = self.user
        with self.assertRaises(Http404):
            self.view(request=request, **{'o_id': 2})

    def test_post_form_correct(self):
        data = deepcopy(self.form_data)
        request = self.factory.post(path=self.url, data=data)
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = self.view(request, **{'o_id': 1})
        count = Review.objects.all().count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, 302)

    def test_post_form_error_zipcode(self):
        data = deepcopy(self.form_data)
        data.update({'zipcode': 123456})
        request = self.factory.post(path=self.url, data=data)
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = self.view(request, **{'o_id': 1})
        count = Review.objects.all().count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, 200)

    def test_post_form_error_email(self):
        data = deepcopy(self.form_data)
        data.update({'email': 'adlxl.alo'})
        request = self.factory.post(path=self.url, data=data)
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = self.view(request, **{'o_id': 1})
        count = Review.objects.all().count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, 200)

    def test_post_not_exist_id(self):
        data = deepcopy(self.form_data)
        request = self.factory.post(path=self.url, data=data)
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        with self.assertRaises(Http404):
            self.view(request, **{'o_id': 2})

    def test_post_anonymous(self):
        data = deepcopy(self.form_data)
        request = self.factory.post(path=self.url, data=data)
        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = self.view(request, **{'o_id': 1})
        count = Review.objects.all().count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, 302)

