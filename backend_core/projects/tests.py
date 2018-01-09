# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

from django.test import TestCase, Client
from django.shortcuts import reverse


from bs4 import BeautifulSoup

from users.models import User, ProfessionalProfile
from .models import Project, Milestone, WAITING
from professionals.models import Professional
from contractors.models import Contractor


class ProjectTest(TestCase):
    def set_user(self):
        self.consumer_password = 'zlxvnlzdgf'
        self.consumer = User.objects.create(
            username='abcde',
            email='zxca@avc.za',
            password=self.consumer_password,
            hoome_id=123,
            role='CONSUMER',
        )
        self.consumer.set_password(self.consumer_password)
        self.consumer.save()
        self.professional = User.objects.create(
            username='qwer',
            email='oqjc@alz.xc',
            password='nvcmxalo',
            hoome_id=321,
            role='PROFESSIONAL',
        )
        self.professional_ = Professional.objects.create(
            lic_num=111,
            name='qqq',
            entity_type='Corporation',
            type='CONTRACTOR',
            state='xxx',
            lic_type='rrr',
            county='iii',
            postal_code='ppp',
        )
        ProfessionalProfile.objects.create(
            professional=self.professional_,
            user=self.professional
        )
        self.contractor = Contractor.objects.create(**{
            'lic_num': 111,
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
        })

    def set_project_data(self):
        self.project_data = {
            'created_by': self.consumer.role,
            'professional_hoome_id': 321,
            'project_name': 'zzz',
            'project_type': 'R',
            'contract_price': 12345,
            'start_date_year': 2000,
            'start_date_month': 1,
            'start_date_day': 2,
            'end_date_year': 2111,
            'end_date_month': 3,
            'end_date_day': 22,
            'first_name': 'qqq',
            'last_name': 'ppp',
            'project_description': 'xxx',
            'form-0-amount': 99999,
            'form-TOTAL_FORMS': 1,
            'form-MAX_NUM_FORMS': 1000,
            'form-MIN_NUM_FORMS': 0,
            'form-INITIAL_FORMS': 0,
        }

    def setUp(self):
        self.client = Client()
        self.set_user()
        self.create_project_path = '/project/create/'
        self.project_detail_path = '/project/{uuid}/'
        self.set_project_data()

    def test_get_create_project(self):
        resp = self.client.get(path=self.create_project_path)
        self.assertEqual(resp.status_code, 200)
        soup = BeautifulSoup(resp.content, 'html.parser')
        title = soup.find(name='h1', class_='section-title').get_text()
        self.assertEqual(title, 'Create Project')

    def test_post_create_project(self):
        project_num = Project.objects.count()
        self.assertEqual(project_num, 0)
        resp = self.client.post(path=self.create_project_path, data=self.project_data)
        self.assertEqual(resp.status_code, 302)
        project = Project.objects.all().order_by('created_at').first()
        self.assertEqual(resp.url, '/project/' + project.uuid)
        self.assertEqual(project.user, None)

    def test_get_project_detail(self):
        self.client.post(path=self.create_project_path, data=self.project_data)
        project = Project.objects.all().first()
        path = self.project_detail_path.format(uuid=project.uuid)
        resp = self.client.get(path=path)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse('account_login') + '?next=/project/{uuid}/'.format(uuid=project.uuid))
        self.client.login(
            username=self.consumer.username,
            password=self.consumer_password,
        )
        resp = self.client.get(path=path)
        self.assertEqual(resp.status_code, 200)
        project = Project.objects.all().first()
        milestone = Milestone.objects.all().first()
        self.assertEqual(project.user, self.consumer)
        soup = BeautifulSoup(resp.content, 'html.parser')
        project_info = soup.find(name='span', class_='title', text='Project Name:').find_parent().get_text()
        project_info = filter(lambda x: x != '', project_info.replace(' ', '').split('\n'))
        self.assertEqual(project_info[0], 'ProjectName:' + project.project_name)
        self.assertEqual(project_info[2], self.professional_.name)
        self.assertEqual(project_info[3], 'ProjectType:' + "REMODEL")
        project_info = soup.find(name='span', class_='title', text='Start Date:').find_parent().get_text()
        project_info = filter(lambda x: x != '', project_info.replace(' ', '').split('\n'))
        start_date = '{month}.{date},{year}'.format(
            month=project.start_date.strftime('%b'),
            date=project.start_date.day,
            year=project.start_date.year,
        )
        end_date = '{month}.{date},{year}'.format(
            month=project.end_date.strftime('%b'),
            date=project.end_date.day,
            year=project.end_date.year,
        )
        self.assertEqual(project_info[0], 'StartDate:' + start_date)
        self.assertEqual(project_info[1], 'EndDate:' + end_date)
        milestone_amount = soup.find(name='table', class_='milestone-table desktop').find(name='td').find_next_sibling()
        self.assertEqual(milestone_amount.get_text(), str(milestone.amount))
        milestone_status = milestone_amount.find_next_sibling().get_text().strip()
        milestone_status = eval(milestone_status.upper())
        self.assertEqual(milestone_status, milestone.status)





