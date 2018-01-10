# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

from django.test import TestCase, Client

from bs4 import BeautifulSoup

from .models import Contractor, BondHistory, BondCompany, WorkerCompensationHistory, InsuranceCompany
from professionals.tests import ProfessionalTest
from review.models import Review
from hscore.models import Hscore


class ContractorTest(ProfessionalTest, TestCase):

    def set_professional_params(self):
        model_params = {
            'lic_num': 1,
            'lic_name': 'bbb',
            'lic_type': 'ccc',
            'lic_status': 'zzz',
            'lic_issue_date': date(2000, 1, 1),
            'lic_expire_date': date(2222, 2, 2),
            'entity': 'aaa',
            'street_address': 'eee',
            'csp': 'fff',
            'state': 'hhh',
            'pos_code': 'jjj',
            'phone': 'yyy',
            'bus_info_add': 'xxx',
            'lic_status_add': 'www',
            'dba': 'iii',
            'uuid': 'kkk',
        }
        return model_params

    def set_model(self):
        self.model = Contractor

    def set_path(self):
        self.path = '/contractor/1/'
        self.path_404 = '/contractor/2/'

    def set_bond_company(self):
        bond_company_params = {
            'surety_code': 'qwe',
            'surety_name': 'ewq',
            'address': 'zxcv',
            'county': 'zxqa',
            'state': 'sdf',
            'pos_code': 'qppl',
        }
        self.bond_company = BondCompany.objects.create(**bond_company_params)

    def set_bond_history(self):
        bond_history_params = {
            'contractor': self.professional,
            'surety_code': self.bond_company,
            'surety_company': 'xolp',
            'bond_num': 'qppz',
            'bond_amount': 'zxvqtj',
            'bond_effective_date': date(2135, 3, 6),
            'bond_cancellation_date': date(2155, 1, 3),
        }
        self.bond_history = BondHistory.objects.create(**bond_history_params)

    def set_issurance_company(self):
        insurance_company_params = {
            'insur_code': 'povz',
            'insur_name': 'qweoox',
            'address': 'mmhjh',
            'county': 'llppq',
            'state': 'lpuyuq',
            'pos_code': 'ouch',
        }
        self.insurance_company = InsuranceCompany.objects.create(**insurance_company_params)

    def set_wc_history(self):
        wc_history_params = {
            'contractor': self.professional,
            'insur_code': self.insurance_company,
            'insur_company': 'zoooz',
            'policy_num': 'zxooxv',
            'insur_effective_date': date(2331, 3, 4),
            'insur_cancellation_date': date(2212, 5, 6),
        }
        self.wc_history = WorkerCompensationHistory.objects.create(**wc_history_params)

    def set_h_score(self):
        h_score_params = {
            'score': 9999,
            'rank': 1,
            'max': 99999,
            'contractor': self.professional
        }
        self.h_score = Hscore.objects.create(**h_score_params)

    def setUp(self):
        self.client = Client()
        self.set_user()
        self.set_professional_params()
        self.set_path()
        self.set_model()
        self.professional = self.model.objects.create(**self.set_professional_params())
        self.review = Review.objects.create(**self.set_review_params())
        self.set_user_ratings()
        self.set_bond_company()
        self.set_bond_history()
        self.set_issurance_company()
        self.set_wc_history()
        self.set_h_score()
        self.set_professional_user()
        self.resp = self.client.get(path=self.path)
        self.soup = BeautifulSoup(self.resp.content, 'html.parser')

    def test_get_lic_num(self):
        lic_num = self.soup.find(name='td', class_='rname', text='License #:').find_next_sibling().get_text()
        self.assertEqual(self.professional.lic_num, int(lic_num))

    def test_get_lic_type(self):
        lic_type = self.soup.find(name='td', class_='rname', text='License Type:').find_next_sibling().get_text()
        self.assertEqual(self.professional.lic_type + ' ', lic_type)

    def test_get_lic_status(self):
        lic_status = self.soup.find(name='td', class_='rname', text=' License Status:').find_next_sibling().get_text()
        self.assertEqual(self.professional.lic_status, lic_status)

    def test_get_lic_issue_date(self):
        issued_date = self.soup.find(name='td', class_='rname', text='Issued Date:').find_next_sibling().get_text()
        lic_issued_date = '{month}. {date}, {year}'.format(
            month=self.professional.lic_issue_date.strftime('%b'),
            date=self.professional.lic_issue_date.day,
            year=self.professional.lic_issue_date.year,
        )
        self.assertEqual(lic_issued_date, issued_date)

    def test_get_entity(self):
        entity = self.soup.find(name='td', class_='rname', text='Entity:').find_next_sibling().get_text()
        self.assertEqual(self.professional.entity, entity)

    def test_get_bond_company(self):
        bond_company = self.soup.find(name='td', class_='rname', text='Bonded:').find_next_sibling().get_text()
        self.assertEqual(self.bond_history.surety_company, bond_company)

    def test_get_wc_history(self):
        wc_history = self.soup.find(name='td', class_='rname', text='Issued:').find_next_sibling().get_text()
        self.assertEqual(self.wc_history.insur_company, wc_history)

    def test_get_phone(self):
        pass

    def test_get_lic_address(self):
        address = self.soup.find(name='td', class_='rname', text='Address:').find_next_sibling().get_text()
        address = address.replace('\n', ',', 1).replace(' ', '').replace('\n', '')
        address = filter(lambda x: x != '', address)
        street_address, csp = address.split(',')[0:2]
        self.assertEqual(self.professional.street_address, street_address)
        self.assertEqual(self.professional.csp, csp)

    def test_h_score(self):
        h_score = self.soup.find(name='li', attrs={'id': 'score-popup', 'class': 'popup'}).get_text().replace(' ', '')
        h_score = filter(lambda x: x != '',  h_score.split('\n'))
        h_score = h_score[0]
        self.assertEqual('HoomeScore:{h_score}'.format(h_score=self.h_score.score), h_score)
