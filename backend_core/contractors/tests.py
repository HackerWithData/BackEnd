from __future__ import unicode_literals
import datetime

from django.test import TestCase, RequestFactory

from .models import Contractor, ComplaintOverall
from .utils import get_contractor_lic_length, get_complaint


class ContractorTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.contractor = Contractor.objects.create(
            lic_num=1,
            lic_expire_date=datetime.date(2100, 12, 31),
            lic_issue_date=datetime.date(2000, 1, 1),
            lic_status='Active',
            lic_type='CONTRACTOR',
        )

    def test_get_contractor_lic_length(self):
        length = get_contractor_lic_length(contractor=self.contractor)
        self.assertEqual(length, datetime.date.today().year - self.contractor.lic_issue_date.year)

    def test_get_complaint(self):
        c1 = get_complaint(contractor=self.contractor)
        c2 = ComplaintOverall.objects.get(contractor=self.contractor)
        self.assertEqual(c1, c2)
