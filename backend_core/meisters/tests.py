# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from .models import Meister
from professionals.tests import ProfessionalTest


class MeisterTest(ProfessionalTest, TestCase):

    def set_professional_params(self):
        model_params = {
            'lic_num': 1,
            'lic_name': 'bbb',
            'bus_name': 'aaa',
            'street_address': 'eee',
            'county': 'iii',
            'state': 'hhh',
            'pos_code': 'jjj',
            'phone': 'zzz'
        }
        return model_params

    def set_model(self):
        self.model = Meister

    def set_path(self):
        self.path = '/meister/1/'
        self.path_404 = '/meister/2/'

    def test_get_phone(self):
        phone = self.soup.find(name='li', text='Phone: ' + self.professional.phone)
        self.assertNotEqual(phone, None)

    def test_get_lic_address(self):
        address = self.soup.find(name='td', class_='rname', text='Address:').find_next_sibling().get_text()
        address = address.split('\n')
        address = filter(lambda x: x != '', address)
        street_address = address[0].strip()
        self.assertEqual(street_address, self.professional.street_address)
        address = address[1].split(',')
        county = address[0].strip()
        self.assertEqual(county, self.professional.county)
        state, pos_code = address[1].strip().split(' ')
        self.assertEqual(state, self.professional.state)
        self.assertEqual(pos_code, self.professional.pos_code)
