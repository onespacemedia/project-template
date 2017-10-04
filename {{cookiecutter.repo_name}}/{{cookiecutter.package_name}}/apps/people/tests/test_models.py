from cms.apps.pages.models import Page
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from ..models import People, Person


class ApplicationTestCase(TestCase):
    def setUp(self):
        # Note: as this is the only page in the database, it's absolute URL
        # will simply be '/'

        content_type = ContentType.objects.get_for_model(People)
        self.page = Page.objects.create(
            content_type=content_type,
            title='Foo',
            slug='foo',
        )

        self.person_page = People.objects.create(
            page=self.page,
        )

        self.person = Person.objects.create(
            page=self.person_page,
            slug='foo-bar',
            first_name='Foo',
            last_name='Bar',
        )

    def test_person_get_absolute_url(self):
        self.assertEqual(self.person.get_absolute_url(), '/foo-bar/')

    def test_person_unicode(self):
        self.assertEqual(self.person.__str__(), 'Foo Bar')
