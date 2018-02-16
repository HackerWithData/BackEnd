# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
import os

from django.test import Client, TestCase
from django.contrib.contenttypes.models import ContentType

from bs4 import BeautifulSoup

from review.models import Review
from users.models import User, ProfessionalProfile
from ratings.models import UserRating
from professionals.models import Professional, DataCollection
from datasources.models import DataSourceElpaso
from photos.models import BackgroundPhoto, Photo
from projects.models import PROJECT_TYPE


class ProfessionalViewTest(TestCase):
    uuid = 'db9d6282-344c-4541-8b10-88f66e57878a'

    def _set_path(self):
        self.path = '/professional/{uuid}/'.format(uuid=self.uuid)
        self.path_404 = '/professional/97caaf5f-b40f-43d4-86a1-639e0b657d8e/'

    def _set_datasource(self):
        DataSourceElpaso.objects.create(
            lic_num=123,
            lic_type='Architect',
            type='Architect',
            name='ppp',
            lic_state='zxc',
            lic_board='lll',
            lic_status='ooo',
            address='nnn',
            state_lic_num='iii',
            name2='ttt',
            phone=123456678,
            email='zxcvukiha@sdk.ckka',
            lic_issue_date=date(2000, 1, 1),
            lic_expire_date=date(2222, 2, 2),
            bus_expire_date=date(2333, 3, 3),
            insur_company='xiooq',
            insur_policy='zoiooq',
        )

    def _set_datacollection(self):
        DataCollection.objects.create(
            object_id=1,
            lic_num=123,
            content_type_id=ContentType.objects.get(model='datasourceelpaso').id,
            professional_id=1
        )

    def _set_professional(self):
        self.professional = Professional.objects.create(
            name='zzz',
            owner_name='xxx',
            csp='bbb',
            address1='ccc',
            address2='ddd',
            county='qqq',
            lic_status='A',
            phone='123456789',
            entity_type='Corporation',
            state='xvaqwe',
            pos_code='12345',
            uuid='db9d6282-344c-4541-8b10-88f66e57878a',
        )

    def _set_client(self):
        self.client = Client()

    def _set_user(self):
        self.password = 'zlxvnlzdgf'
        self.user = User.objects.create(
            username='abcde',
            email='zxca@avc.za',
            password='qqq',
            hoome_id=123,
            role='PROFESSIONAL',
        )
        self.user.set_password(self.password)
        self.user.save()
        ProfessionalProfile.objects.create(
            professional=self.professional,
            user=self.user
        )

    def setUp(self):
        self._set_datacollection()
        self._set_datasource()
        self._set_professional()
        self._set_path()
        self._set_client()
        self._set_user()

    def test_professional_view(self):
        resp = self.client.get(path=self.path)
        self.assertEqual(resp.status_code, 200)
        resp_404 = self.client.get(path=self.path_404)
        soup_404 = BeautifulSoup(resp_404.content, 'html.parser')
        self.assertEqual(
            soup_404.find(name='div', class_='container header-gap').find(name='h1').get_text(), 'Page Not Found'
        )
        soup = BeautifulSoup(resp.content, "html.parser")
        self.assertEqual(soup.find(name='span', class_='bus-name').get_text(), self.professional.name)
        contact_info = soup.find(name='div', class_='horizontal-list').get_text()
        self.assertIn(self.professional.csp, contact_info)
        self.assertIn(self.professional.phone, contact_info)
        business_info = soup.find_all(name='td', class_='rname')
        lic_status = business_info[0].find_next_sibling().get_text()
        self.assertEqual(lic_status, self.professional.lic_status)
        lic_type = business_info[1].find_next_sibling().get_text()
        self.assertEqual(lic_type, self.professional.entity_type)
        address_info = business_info[2].find_next_sibling().get_text()
        address, csp = address_info.split('\n', 1)
        address = address.strip()
        csp = csp.strip()
        self.assertEqual(address, self.professional.address1 + ' ' + self.professional.address2)
        self.assertEqual(csp, self.professional.csp)

    def test_post_review(self):
        self.review_data = {
            'comments': 'pp',
            'first_name': 'oo',
            'last_name': 'ii',
            'project_date_year': 1999,
            'project_date_month': 12,
            'project_date_day': 3,
            'project_type': 'R',
            'project_cost': '654321',
            'project_duration': '99',
            'email': 'ww@ee.cc',
            'street_address': 'uu',
            'street_address2': 'tt',
            'county': 'mm',
            'state': 'nn',
            'zipcode': '12345',
            'is_anonymous': False,
            'review': 'review',
            'q_rating': '6',
            'l_rating': '7',
            'e_rating': '7',
        }
        resp = self.client.post(path=self.path, data=self.review_data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)
        resp = self.client.get(self.path)
        soup = BeautifulSoup(resp.content, 'html.parser')
        reviews = soup.find_all(name='div', class_='user-review')
        review = reviews[0].find(name='div', class_='main-spec').get_text()
        user_rating = reviews[0].find(name='div', class_='user-rating').get_text()
        project_type = [i[1] for i in PROJECT_TYPE if i[0] == self.review_data.get('project_type')][0]
        project_type = str(project_type)
        self.assertIn('Project Cost: ' + self.review_data.get('project_cost'), review)
        self.assertIn('Project Type: ' + project_type, review)
        self.assertIn('Project Duration: ' + self.review_data.get('project_duration'), review)
        self.assertIn(self.review_data.get('comments'), review)
        self.assertIn('Quality : ' + self.review_data.get('q_rating'), user_rating)
        self.assertIn('Length : ' + self.review_data.get('l_rating'), user_rating)
        self.assertIn('Efficiency : ' + self.review_data.get('e_rating'), user_rating)

    def test_upload_bgimage(self):
        path = self.path + 'background-upload'
        resp = self.client.get(path=path)
        soup = BeautifulSoup(resp.content, 'html.parser')
        error_message = soup.find(name='div', class_='container header-gap').find(name='p').get_text().strip()
        self.assertEqual(error_message, 'Hoome cannot find the page per your request, Please try again.')
        self.client.login(
            username=self.user.username,
            password=self.password,
        )

        pic_1 = str(os.getcwd()) + '/static/image/background-pic/home-gradient.png'
        pic_2 = str(os.getcwd()) + '/static/image/background-pic/home-gradient-2.png'
        with open(pic_1, 'r') as f:
            resp = self.client.post(path=path, data={
                'img': f,
            })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(BackgroundPhoto.objects.count(), 1)
        resp = self.client.get(path=self.path)
        soup = BeautifulSoup(resp.content, 'html.parser')
        bg_image = BackgroundPhoto.objects.all().first()
        self.assertIn(bg_image.img.url, soup.find(name='style').get_text())
        with open(pic_2, 'r') as f:
            resp = self.client.post(path=path, data={
                'img': f,
            })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(BackgroundPhoto.objects.count(), 1)
        resp = self.client.get(path=self.path)
        soup = BeautifulSoup(resp.content, 'html.parser')
        bg_image = BackgroundPhoto.objects.all().first()
        self.assertIn(bg_image.img.url, soup.find(name='style').get_text())

    def test_upload_project_photo(self):
        path = self.path + 'project-photos/upload'
        resp = self.client.get(path=path)
        soup = BeautifulSoup(resp.content, 'html.parser')
        error_message = soup.find(name='div', class_='container header-gap').find(name='p').get_text().strip()
        self.assertEqual(error_message, 'Hoome cannot find the page per your request, Please try again.')
        self.client.login(
            username=self.user.username,
            password=self.password,
        )
        pic_1 = str(os.getcwd()) + '/static/image/background-pic/home-gradient.png'
        pic_2 = str(os.getcwd()) + '/static/image/background-pic/home-gradient-2.png'
        with open(pic_1, 'r') as f:
            resp = self.client.post(path=path, data={
                'img': f,
            })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Photo.objects.count(), 1)
        with open(pic_2, 'r') as f:
            resp = self.client.post(path=path, data={
                'img': f,
            })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Photo.objects.count(), 2)
        resp = self.client.get(path=self.path)
        soup = BeautifulSoup(resp.content, 'html.parser')
        images = soup.find(name='div', class_='popup-gallery').find_all(name='img')
        images = [image.get('src', '') for image in images]
        photos = Photo.objects.all()
        for photo in photos:
            self.assertIn(photo.img.url, images)


