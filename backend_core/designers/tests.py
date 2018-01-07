# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

from django.test import TestCase

from .models import Designer
from professionals.tests import ProfessionalTest


class DesignerTest(ProfessionalTest, TestCase):

    def set_professional_params(self):
        model_params = {
            'lic_num': 1,
            'lic_name': 'bbb',
            'lic_type': 'ccc',
            'lic_status': 'ddd',
            'street_address': 'eee',
            'city': 'fff',
            'state': 'hhh',
            'country': 'iii',
            'pos_code': 'jjj',
            'uuid': 'kkk',
            'bus_name': 'aaa',
            'office_location_name': 'ooo',
            'website': 'ppp',
            'phone': '134566',
            'mobile': '092137',
            'fax': '1293901',
            'email': 'qqqq@pppp.cccc',
            'state_designer_num': 'ttt',
            'contractor_lic_num': 'rrr',
        }
        return model_params

    def set_model(self):
        self.model = Designer

    def set_path(self):
        self.path = '/designer/1/'
