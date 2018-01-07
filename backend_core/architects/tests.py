# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

from django.test import TestCase

from bs4 import BeautifulSoup

from .models import Architect
from professionals.tests import ProfessionalTest


class ArchitectTests(ProfessionalTest, TestCase):

    def set_professional_params(self):
        model_params = {
            'lic_num': 1,
            'lic_prefix': 'aaa',
            'lic_name': 'bbb',
            'lic_type': 'ccc',
            'lic_status': 'ddd',
            'lic_issue_date': date(2000, 1, 1),
            'lic_expire_date': date(2222, 2, 2),
            'street_address': 'eee',
            'city': 'fff',
            'county': 'ggg',
            'state': 'hhh',
            'country': 'iii',
            'pos_code': 'jjj',
            'uuid': 'kkk',
        }
        return model_params

    def set_model(self):
        self.model = Architect

    def set_path(self):
        self.path = '/architect/1/'

