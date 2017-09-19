# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, RequestFactory
from django.test import TestCase

from models import User, ConsumerProfile, ProfessionalProfile
from utils import *


class UserTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.consumer = User.objects.create_user(username='test.user', email='test.user@gmail.com',
                                             password='testing1', role=CONSUMER)
        # self.consumer_profile = ConsumerProfile.objects.create(z)

    # def test_animals_can_speak(self):
    #     """Animals that can speak are correctly identified"""
    #     lion = Animal.objects.get(name="lion")
    #     cat = Animal.objects.get(name="cat")
    #     self.assertEqual(lion.speak(), 'The lion says "roar"')
    #     self.assertEqual(cat.speak(), 'The cat says "meow"')