# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from django.http import Http404

from architects.models import Architect
from .utils import get_professional_instance
from .models import Professional
from .views import ProfessionalDetail


class ProfessionalTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Architect.objects.create(lic_num=1234)
        Architect.objects.create(lic_num=4321)
        Professional.objects.create(lic_num=1234, type='ARCHITECT')
        Professional.objects.create(lic_num=4321, type='ARCHITECT')

    def test_get_professional_instance(self):
        i1 = get_professional_instance(model_type='architect', lic_num=1234)
        i2 = Architect.objects.get(lic_num=1234)
        i3 = Architect.objects.get(lic_num=4321)
        self.assertEqual(i1, i2)
        self.assertNotEqual(i1, i3)

    def test_professional_detail(self):
        request = self.factory.get('/architect/1234/')
        view = ProfessionalDetail.as_view(
            data_source='California Architects Board',
            template_name='architect/architect.html',
            model_name='architect',
        )
        response = view(request=request, **{'o_id': 1234})
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Http404):
            view(request=request, **{'o_id': 1111})
