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
            'bus_name': 'aaa',
            'office_location_name': 'ooo',
            'website': 'ppp',
            'phone': '134566',
            'mobile': '092137',
            'fax': '1293901',
            'email': 'qqqq@pppp.cccc',
            'state_designer_num': 'ttt',
            'contractor_lic_num': 'rrr',
            'street_address': 'eee',
            'city': 'fff',
            'state': 'hhh',
            'country': 'iii',
            'pos_code': 'jjj',
            'uuid': 'kkk',
        }
        return model_params

    def set_model(self):
        self.model = Designer

    def set_path(self):
        self.path = '/designer/1/'
        self.path_404 = '/designer/2/'

    def test_get_lic_num(self):
        lic_num = self.soup.find(name='td', class_='rname', text='License #:').find_next_sibling().get_text()
        self.assertEqual(self.professional.lic_num, int(lic_num))

    def test_get_lic_type(self):
        lic_type = self.soup.find(name='td', class_='rname', text='License Type:').find_next_sibling().get_text()
        self.assertEqual(self.professional.lic_type + ' ', lic_type)

    def test_get_bus_name(self):
        bus_name = self.soup.find(name='td', class_='rname', text='Company Name:').find_next_sibling().get_text()
        self.assertEqual(bus_name, self.professional.bus_name)

    def test_get_state_designer_num(self):
        state_designer_num = self.soup.find(name='td', class_='rname', text='State Designer Num:').find_next_sibling().get_text()
        self.assertEqual(state_designer_num, self.professional.state_designer_num)

    def test_get_contractor_lic_num(self):
        contractor_lic_num = self.soup.find(name='td', class_='rname', text='Contractor Licence Num:').find_next_sibling().get_text()
        self.assertEqual(contractor_lic_num, self.professional.contractor_lic_num)

    def test_get_phone(self):
        phone = self.soup.find(name='td', class_='rname', text='Phone:').find_next_sibling().get_text()
        self.assertEqual(phone, self.professional.phone)

    def test_get_mobile(self):
        mobile = self.soup.find(name='td', class_='rname', text='Mobile:').find_next_sibling().get_text()
        self.assertEqual(mobile, self.professional.mobile)

    def test_get_fax(self):
        fax = self.soup.find(name='td', class_='rname', text='Fax:').find_next_sibling().get_text()
        self.assertEqual(fax, self.professional.fax)

    def test_get_lic_address(self):
        address = self.soup.find(name='td', class_='rname', text='Address:').find_next_sibling().get_text()
        address = address.replace('\n', ',', 1).replace(' ', '').replace('\n', '')
        address = filter(lambda x: x != '', address)
        street_address, city, state = address.split(',')[0:3]
        self.assertEqual(self.professional.street_address, street_address)
        self.assertEqual(self.professional.city, city)
        self.assertEqual(self.professional.state, state)
