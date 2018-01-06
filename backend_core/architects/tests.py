# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from .models import Architect
from professionals.tests import ProfessionalTest


class ArchitectTests(ProfessionalTest, TestCase):

    def set_model(self):
        self.model = Architect

    def set_path(self):
        self.path = '/architect/1/'

