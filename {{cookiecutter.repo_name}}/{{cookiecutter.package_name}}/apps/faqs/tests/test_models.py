import json

from bs4 import BeautifulSoup
from cms.apps.pages.models import Page
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase
from watson import search

from ..models import Faq, Faqs


class ApplicationTestCase(TestCase):

    def setUp(self):
        # Note: as this is the only page in the database, it's absolute URL
        # will simply be '/'

        with search.update_index():
            content_type = ContentType.objects.get_for_model(Faqs)
            self.page = Page.objects.create(
                content_type=content_type,
                title='Foo',
                slug='foo',
            )

            self.faq_page = Faqs.objects.create(
                page=self.page,
            )

        self.faq = Faq.objects.create(
            page=self.faq_page,
            question='What colour is the sky?',
            answer='Blue',
            slug='what-colour-sky'
        )

    def test_faq_get_absolute_url(self):
        self.assertEqual(self.faq.get_absolute_url(), '/what-colour-sky/')

    def test_faq_unicode(self):
        self.assertEqual(self.faq.__str__(), 'What colour is the sky?')

    def test_schema_generation(self):
        self.client = Client()

        url = self.faq.get_absolute_url()
        response = self.client.get(url)
        soup = BeautifulSoup(response.rendered_content, 'html.parser')

        valid = True
        try:
            _ = json.loads(soup.find('script', type='application/ld+json').text)
        except ValueError:
            valid = False

        self.assertTrue(valid)
