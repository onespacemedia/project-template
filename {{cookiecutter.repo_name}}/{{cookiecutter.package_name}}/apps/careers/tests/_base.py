from datetime import timedelta

from cms.apps.pages.models import Page
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils import timezone
from watson import search

from ..models import Career, Careers


class CareersBaseTestCase(TestCase):

    def setUp(self):
        # Note: as this is the only page in the database, it's absolute URL
        # will simply be '/'

        with search.update_index():
            content_type = ContentType.objects.get_for_model(Careers)
            self.page = Page.objects.create(
                content_type=content_type,
                title='Foo',
                slug='foo',
            )

            self.job_page = Careers.objects.create(
                page=self.page,
            )

        # Add one with no closing date
        self.job = Career.objects.create(
            page=self.job_page,
            slug='foo-bar',
            title='Tester',
            # Make sure b
        )

        # Add one with a past closing date.
        self.closed_job = Career.objects.create(
            page=self.job_page,
            slug='closed-job',
            title='Closed job',
            closing_date=(timezone.now() - timedelta(days=30)).date()
        )

        # Add one with a past closing date.
        self.closes_future_job = Career.objects.create(
            page=self.job_page,
            slug='open-job',
            title='Open job',
            closing_date=(timezone.now() + timedelta(days=30)).date()
        )
