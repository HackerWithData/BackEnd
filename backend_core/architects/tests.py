# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

from django.test import TestCase

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
        self.path_404 = '/architect/2/'

    def test_get_lic_num(self):
        lic_num = self.soup.find(name='td', class_='rname', text='License #:').find_next_sibling().get_text()
        self.assertEqual(self.professional.lic_num, int(lic_num))

    def test_get_lic_type(self):
        lic_type = self.soup.find(name='td', class_='rname', text='License Type:').find_next_sibling().get_text()
        self.assertEqual(self.professional.lic_type + ' ', lic_type)

    def test_get_lic_address(self):
        address = self.soup.find(name='td', class_='rname', text='Address:').find_next_sibling().get_text()
        address = address.replace('\n', ',', 1).replace(' ', '').replace('\n', '')
        address = filter(lambda x: x != '', address)
        street_address, city, state = address.split(',')[0:3]
        self.assertEqual(self.professional.street_address, street_address)
        self.assertEqual(self.professional.city, city)
        self.assertEqual(self.professional.state, state)

    def test_get_lic_issue_date(self):
        issued_date = self.soup.find(name='td', class_='rname', text='Issued Date:').find_next_sibling().get_text()
        lic_issued_date = '{month}. {date}, {year}'.format(
            month=self.professional.lic_issue_date.strftime('%b'),
            date=self.professional.lic_issue_date.day,
            year=self.professional.lic_issue_date.year,
        )
        self.assertEqual(lic_issued_date, issued_date)

    def test_get_lic_status(self):
        lic_status = self.soup.find(name='td', class_='rname', text='License Status:').find_next_sibling().get_text()
        self.assertEqual(self.professional.lic_status, lic_status)
