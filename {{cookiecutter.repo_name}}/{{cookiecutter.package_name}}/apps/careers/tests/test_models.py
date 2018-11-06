import json
from datetime import timedelta

from bs4 import BeautifulSoup
from django.test import Client
from django.utils import timezone

from ..models import Career
from ._base import CareersBaseTestCase


class CareerModelsTestCase(CareersBaseTestCase):

    def test_job_get_absolute_url(self):
        self.assertEqual(self.job.get_absolute_url(), '/foo-bar/')

    def test_job_unicode(self):
        self.assertEqual(self.job.__str__(), 'Tester')

    def test_careerqueryset_select_open(self):
        # Make sure jobs with no closing date are considered as open.
        self.assertIn(self.job, Career.objects.all().select_open())
        # Make sure one with a closing date in the future are considered as
        # open.
        self.assertIn(self.closes_future_job, Career.objects.all().select_open())
        # Make sure those which have a closing date in the past are not
        # considered as open.
        self.assertNotIn(self.closed_job, Career.objects.all().select_open())

    def test_careerqueryset_select_closed(self):
        # Make sure those which have a closing date in the past are considered
        # as closed.
        self.assertIn(self.closed_job, Career.objects.all().select_closed())

        # Make sure jobs with no closing date are not considered to be closed.
        self.assertNotIn(self.job, Career.objects.all().select_closed())

        # Make sure one with a closing date in the future are not considered
        # as closed.
        self.assertNotIn(self.closes_future_job, Career.objects.all().select_closed())

    def test_career_is_open(self):
        self.assertTrue(self.job.is_open())
        self.assertTrue(self.closes_future_job.is_open())
        self.assertFalse(self.closed_job.is_open())

    def test_schema_generation(self):
        self.client = Client()

        url = self.closes_future_job.get_absolute_url()
        response = self.client.get(url)
        soup = BeautifulSoup(response.rendered_content, 'html.parser')

        valid = True
        try:
            _ = json.loads(soup.find('script', type='application/ld+json').text)
        except ValueError:
            valid = False

        self.assertTrue(valid)
