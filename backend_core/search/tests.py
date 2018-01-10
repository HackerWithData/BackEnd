# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

from django.test import TestCase, Client
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _

from architects.models import Architect
from contractors.models import Contractor
from designers.models import Designer
from meisters.models import Meister
from professionals.models import Professional, ProfessionalType
from.search_helpers import UndefinedProfessionalType


class SearchTest(TestCase):

    def set_architect(self):
        self.architect = Architect.objects.create(**{
            'lic_num': 1,
            'lic_prefix': 'aaaa',
            'lic_name': 'abbb',
            'lic_type': 'accc',
            'lic_status': 'addd',
            'lic_issue_date': date(2000, 1, 1),
            'lic_expire_date': date(2222, 2, 2),
            'street_address': 'aeee',
            'city': 'afff',
            'county': 'aggg',
            'state': 'ahhh',
            'country': 'aiii',
            'pos_code': '123',
            'uuid': 'akkk',
        })
        professional = Professional.objects.create(**{
            'lic_num': 1,
            'name': self.architect.lic_name,
            'entity_type': 'aaazxxc',
            'type': 'ARCHITECT',
            'state': 'zxxv',
            'lic_type': 'zxhrf',
            'postal_code': '123',
            'county': 'zxcv',
        })
        ProfessionalType.objects.create(
            professional=professional,
            type=professional.type,
            subtype=_('Architect'),
        )

    def set_contractor(self):
        self.contractor = Contractor.objects.create(**{
            'lic_num': 1,
            'lic_name': 'cbbb',
            'lic_type': 'cccc',
            'lic_status': 'czzz',
            'lic_issue_date': date(2000, 1, 1),
            'lic_expire_date': date(2222, 2, 2),
            'entity': 'caaa',
            'street_address': 'ceee',
            'csp': 'cfff',
            'state': 'chhh',
            'pos_code': '123',
            'phone': 'cyyy',
            'bus_info_add': 'cxxx',
            'lic_status_add': 'cwww',
            'dba': 'ciii',
            'uuid': 'ckkk',
        })
        professional = Professional.objects.create(**{
            'lic_num': 1,
            'name': self.contractor.lic_name,
            'entity_type': 'aaazxxc',
            'type': 'CONTRACTOR',
            'state': 'zxxv',
            'lic_type': 'zxhrf',
            'postal_code': '123',
            'county': 'zxcv',
        })
        ProfessionalType.objects.create(
            professional=professional,
            type=professional.type,
            subtype=_('General Contractor'),
        )

    def set_designer(self):
        self.designer = Designer.objects.create(**{
            'lic_num': 1,
            'lic_name': 'dbbb',
            'lic_type': 'dccc',
            'bus_name': 'daaa',
            'office_location_name': 'dooo',
            'website': 'dppp',
            'phone': '134566',
            'mobile': '092137',
            'fax': '1293901',
            'email': 'qqqq@pppp.cccc',
            'state_designer_num': 'dttt',
            'contractor_lic_num': 'drrr',
            'street_address': 'deee',
            'city': 'dfff',
            'state': 'dhhh',
            'country': 'diii',
            'pos_code': '123',
            'uuid': 'dkkk',
        })
        professional = Professional.objects.create(**{
            'lic_num': 1,
            'name': self.designer.lic_name,
            'entity_type': 'aaazxxc',
            'type': 'DESIGNER',
            'state': 'zxxv',
            'lic_type': 'zxhrf',
            'postal_code': '123',
            'county': 'zxcv',
        })
        ProfessionalType.objects.create(
            professional=professional,
            type=professional.type,
            subtype=_('Designer'),
        )

    def set_meister(self):
        self.meister = Meister.objects.create(**{
            'lic_num': 1,
            'lic_name': 'mbbb',
            'bus_name': 'maaa',
            'street_address': 'meee',
            'county': 'miii',
            'state': 'mhhh',
            'pos_code': '123',
            'phone': 'mzzz',
        })
        professional = Professional.objects.create(**{
            'lic_num': 1,
            'name': self.meister.lic_name,
            'entity_type': 'aaazxxc',
            'type': 'MEISTER',
            'state': 'zxxv',
            'lic_type': 'zxhrf',
            'postal_code': '123',
            'county': 'zxcv',
        })
        ProfessionalType.objects.create(
            professional=professional,
            type=professional.type,
            subtype=_('Meister'),
        )

    def setUp(self):
        self.set_architect()
        self.set_contractor()
        self.set_designer()
        self.set_meister()
        self.client = Client()
        self.path = reverse('search_new')
        self.error_msg = 'No professional match your condition. Please try another way to search again.'

    def test_search_by_name_or_lic(self):
        resp = self.client.get(path=self.path, data={
            'type': 'NAMEORLIC',
            'target': '1',
            'zipcode': '000',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.architect.lic_name)
        self.assertContains(resp, self.contractor.lic_name)
        self.assertContains(resp, self.designer.lic_name)
        self.assertContains(resp, self.meister.lic_name)
        resp = self.client.get(path=self.path, data={
            'type': 'NAMEORLIC',
            'target': 'abbb',
            'zipcode': '999',
        })
        self.assertContains(resp, self.architect.lic_name)
        self.assertNotContains(resp, self.contractor.lic_name)
        self.assertNotContains(resp, self.designer.lic_name)
        self.assertNotContains(resp, self.meister.lic_name)
        resp = self.client.get(path=self.path, data={
            'type': 'NAMEORLIC',
            'target': 'xzkvjbafho',
            'zipcode': '999',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.error_msg)
        resp = self.client.get(path=self.path, data={
            'type': 'NAMEORLIC',
            'target': '',
            'zipcode': '999',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, self.path)

    def test_search_by_zipcode(self):
        self.assertRaises(
            excClass=UndefinedProfessionalType,
            callableObj=self.client.get,
            **{
                'path': self.path,
                'data': {
                    'type': '',
                    'target': '1',
                    'zipcode': '123',
                }
            }
        )

        resp = self.client.get(path=self.path, data={
            'type': 'architect',
            'target': '',
            'zipcode': '123',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.architect.lic_name)
        self.assertContains(resp, self.contractor.lic_name)
        self.assertContains(resp, self.designer.lic_name)
        self.assertContains(resp, self.meister.lic_name)

        resp = self.client.get(path=self.path, data={
            'type': 'architect',
            'target': _('Architect'),
            'zipcode': '123',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.architect.lic_name)
        self.assertNotContains(resp, self.contractor.lic_name)
        self.assertNotContains(resp, self.designer.lic_name)
        self.assertNotContains(resp, self.meister.lic_name)

        resp = self.client.get(path=self.path, data={
            'type': 'contractor',
            'target': _('General Contractor'),
            'zipcode': '123',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, self.architect.lic_name)
        self.assertContains(resp, self.contractor.lic_name)
        self.assertNotContains(resp, self.designer.lic_name)
        self.assertNotContains(resp, self.meister.lic_name)

        resp = self.client.get(path=self.path, data={
            'type': 'designer',
            'target': _('Designer'),
            'zipcode': '123',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, self.architect.lic_name)
        self.assertNotContains(resp, self.contractor.lic_name)
        self.assertContains(resp, self.designer.lic_name)
        self.assertNotContains(resp, self.meister.lic_name)

        resp = self.client.get(path=self.path, data={
            'type': 'meister',
            'target': _('Meister'),
            'zipcode': '123',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, self.architect.lic_name)
        self.assertNotContains(resp, self.contractor.lic_name)
        self.assertNotContains(resp, self.designer.lic_name)
        self.assertContains(resp, self.meister.lic_name)






