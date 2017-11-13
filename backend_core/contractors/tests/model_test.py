# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, RequestFactory

import unittest
import mock

from ..models import Contractor


class ContractorTestCase(unittest.TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.contractor = Contractor(username='test.consumer',
                                     email='test.consumer@gmail.com',
                                     password='testing1',
                                     role=CONSUMER)

        # lic_num = models.IntegerField(primary_key=True, unique=True)
        # lic_name = models.CharField(max_length=255)
        # lic_status = models.CharField(max_length=30)
        # lic_issue_date = models.DateField(blank=True, null=True)
        # lic_expire_date = models.DateField(blank=True, null=True)
        # lic_type = models.TextField()
        # entity = models.CharField(max_length=25)
        # street_address = models.CharField(max_length=255)
        # csp = models.CharField(max_length=63, blank=True)
        # state = models.CharField(max_length=63)
        # pos_code = models.CharField(max_length=25)
        # phone = models.CharField(max_length=25, blank=True, null=True)
        # lic_status_add = models.TextField(blank=True, null=True)
        # bus_info_add = models.TextField(blank=True, null=True)
        # dba = models.CharField(max_length=255, blank=True, null=True)

    # def test_animals_can_speak(self):
    #     """Animals that can speak are correctly identified"""
    #     lion = Animal.objects.get(name="lion")
    #     cat = Animal.objects.get(name="cat")
    #     self.assertEqual(lion.speak(), 'The lion says "roar"')
    #     self.assertEqual(cat.speak(), 'The cat says "meow"')