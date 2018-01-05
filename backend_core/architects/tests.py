# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

from django.test import TestCase, Client

from bs4 import BeautifulSoup

from .models import Architect


class ArchitectTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.architect = Architect.objects.create(
            lic_num=1,
            lic_prefix='aaa',
            lic_name='bbb',
            lic_type='ccc',
            lic_status='ddd',
            lic_issue_date=date(1111, 1, 1),
            lic_expire_date=date(2222, 2, 2),
            street_address='eee',
            city='fff',
            county='ggg',
            state='hhh',
            country='iii',
            pos_code='jjj',
            uuid='kkk',
        )

    def test_view(self):
        resp = self.client.get(path='/architect/1/')
        self.assertEqual(resp.status_code, 200)
        soup = BeautifulSoup(resp.content, 'html.parser')

        lic_name = soup.find(name='span', class_='bus-name').get_text()
        self.assertEqual(self.architect.lic_name, lic_name)
        lic_num = soup.find(name='td', class_='rname', text='License #:').find_next_sibling().get_text()
        self.assertEqual(self.architect.lic_num, int(lic_num))
        lic_status = soup.find(name='td', class_='rname', text='License Status:').find_next_sibling().get_text()
        self.assertEqual(self.architect.lic_status, lic_status)
        lic_type = soup.find(name='td', class_='rname', text='License Type:').find_next_sibling().get_text()
        self.assertEqual(self.architect.lic_type + ' ', lic_type)
        issued_date = soup.find(name='td', class_='rname', text='Issued Date:').find_next_sibling().get_text()
        print issued_date
        x = date(1111, 1, 1)
        x.strftime()
