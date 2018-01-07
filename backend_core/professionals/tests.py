# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date

from django.test import Client
from django.contrib.contenttypes.models import ContentType

from bs4 import BeautifulSoup

from review.models import Review
from users.models import User
from ratings.models import UserRating


class ProfessionalTest(object):

    model = None
    path = None

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

    def set_path(self):
        pass

    def set_model(self):
        pass

    def set_user_ratings(self):
        self.user_ratings = {
            'quality': UserRating.objects.create(
                review=self.review,
                rating_type='Q',
                rating_score=9,
            ),
            'efficiency': UserRating.objects.create(
                review=self.review,
                rating_type='E',
                rating_score=8,
            ),
            'length': UserRating.objects.create(
                review=self.review,
                rating_type='L',
                rating_score=6,
            )
        }

    def set_review_params(self):
        review_params = {
            'user': self.user,
            'project_type': 'R',
            'project_date': date(2001, 12, 11),
            'street_address': 'zzz',
            'street_address2': 'yyy',
            'county': 'xxx',
            'state': 'www',
            'zipcode': 'vvv',
            'project_zipcode': 'uuu',
            'project_cost': 88,
            'project_duration': 99,
            'comments': 'ttt',
            'is_anonymous': False,
            'review_status': 'A',
            'object_id': self.professional.lic_num,
            'content_type_id': ContentType.objects.get_for_model(model=self.model).id,
        }
        return review_params

    def set_user(self):
        self.user = User.objects.create_user(
            username='abcde',
            email='zxca@avc.za',
            password='qwer1234',
        )

    def setUp(self):
        self.client = Client()
        self.set_user()
        self.set_professional_params()
        self.set_path()
        self.set_model()
        self.professional = self.model.objects.create(**self.set_professional_params())
        self.review = Review.objects.create(**self.set_review_params())
        self.set_user_ratings()
        self.resp = self.client.get(path=self.path)
        self.soup = BeautifulSoup(self.resp.content, 'html.parser')

    def test_get_status_code(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_professional_get_lic_name(self):
        lic_name = self.soup.find(name='span', class_='bus-name').get_text()
        self.assertEqual(self.professional.lic_name, lic_name)

    def test_professional_get_lic_num(self):
        lic_num = self.soup.find(name='td', class_='rname', text='License #:').find_next_sibling().get_text()
        self.assertEqual(self.professional.lic_num, int(lic_num))

    def test_professional_get_lic_type(self):
        lic_type = self.soup.find(name='td', class_='rname', text='License Type:').find_next_sibling().get_text()
        self.assertEqual(self.professional.lic_type + ' ', lic_type)

    def test_professional_get_lic_address(self):
        address = self.soup.find(name='td', class_='rname', text='Address:').find_next_sibling().get_text()
        address = address.replace('\n', ',', 1).replace(' ', '').replace('\n', '')
        street_address, city, state = address.split(',')[0:3]
        self.assertEqual(self.professional.street_address, street_address)
        self.assertEqual(self.professional.city, city)
        self.assertEqual(self.professional.state, state)

    def test_professional_get_lic_issued_date(self):
        issued_date = self.soup.find(name='td', class_='rname', text='Issued Date:').find_next_sibling().get_text()
        lic_issued_date = '{month}. {date}, {year}'.format(
            month=self.professional.lic_issue_date.strftime('%b'),
            date=self.professional.lic_issue_date.day,
            year=self.professional.lic_issue_date.year,
        )
        self.assertEqual(lic_issued_date, issued_date)

    def test_professional_get_lic_status(self):
        lic_status = self.soup.find(name='td', class_='rname', text='License Status:').find_next_sibling().get_text()
        self.assertEqual(self.professional.lic_status, lic_status)

    def test_get_review(self):
        resp = self.client.get(path=self.path)
        soup = BeautifulSoup(resp.content, 'html.parser')
        reviews = soup.find_all(name='div', class_='user-review')
        self.assertEqual(len(reviews), 1)
        review = reviews[0]
        review_detail = review.find(name='div', class_='main-spec').get_text()
        review_detail = review_detail.replace(' ', '').split('\n')
        review_detail = filter(lambda x: x != '', review_detail)
        self.assertEqual(review_detail[0], 'ProjectCost:' + str(self.review.project_cost))
        self.assertEqual(review_detail[1], 'ProjectType:REMODEL')
        self.assertEqual(review_detail[2], 'ProjectDuration:' + str(self.review.project_duration))
        self.assertEqual(review_detail[3], self.review.comments)
        user_rating = review.find(name='div', class_='user-rating').get_text()
        user_rating_detail = user_rating.replace(' ', '').split('\n')
        user_rating_detail = filter(lambda x: x != '', user_rating_detail)
        self.assertEqual(user_rating_detail[0], 'Quality:' + str(self.user_ratings.get('quality').rating_score))
        self.assertEqual(user_rating_detail[1], 'Efficiency:' + str(self.user_ratings.get('efficiency').rating_score))
        self.assertEqual(user_rating_detail[2], 'Length:' + str(self.user_ratings.get('length').rating_score))

    def test_get_rating_stars(self):
        resp = self.client.get(path=self.path)
        soup = BeautifulSoup(resp.content, 'html.parser')
        rating = soup.find(name='div', class_='ratings_rating').find_all(name='span', class_='yellow')
        rating = len(rating)
        quality_rating = self.user_ratings.get('quality').rating_score
        efficiency_rating = self.user_ratings.get('efficiency').rating_score
        length_rating = self.user_ratings.get('length').rating_score
        professional_rating = (quality_rating + efficiency_rating + length_rating) / 3
        self.assertEqual(rating, professional_rating)

    def test_post_review(self):
        review_data = {
            'last_name': 'aaa',
            'first_name': 'qwe',
            'county': 'bbb',
            'q_rating': 5,
            'e_rating': 4,
            'l_rating': 8,
            'project_type': 'R',
            'project_date_day': 9,
            'zipcode': '12345',
            'comments': 'xcvasf',
            'review': 'review',
            'state': 'zxv',
            'project_duration': 123,
            'email': 'assaf@sla.ca',
            'project_cost': 99999,
            'project_date_month': 12,
            'project_date_year': 2003,
            'is_anonymous': 'on',
            'street_address2': 'bbb',
            'street_address': 'ccc',
        }
        resp = self.client.post(path=self.path, data=review_data)
        self.assertEqual(resp.status_code, 302)
        review = Review.objects.get(email=review_data.get('email'))
        self.assertNotEqual(review, None)
        review_data.pop('review')
        resp = self.client.post(path=self.path, data=review_data)
        print resp.status_code


