from cms.apps.pages.models import Page
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from watson import search

from ..models import Contact


class ContactTestCase(TestCase):
    def _create_objects(self):
        with search.update_index():
            self.page = Page.objects.create(
                title='Contact test',
                content_type=ContentType.objects.get_for_model(Contact),
            )

            self.contact = Contact.objects.create(
                page=self.page,
                form_email_address='',
            )

    def test_contact(self):
        self._create_objects()
        tests = [
            # Test with commas, spaces, excessive spaces, etc.
            ('test@test.com', ['test@test.com']),
            ('   test@test.com  ', ['test@test.com']),
            ('test@test.com,', ['test@test.com']),
            ('test@test.com,test2@test.com', ['test@test.com', 'test2@test.com']),
            ('test@test.com, test2@test.com', ['test@test.com', 'test2@test.com']),
            ('test@test.com test2@test.com', ['test@test.com', 'test2@test.com']),
            ('   test@test.com    test2@test.com  ', ['test@test.com', 'test2@test.com']),
            ('   test@test.com  , test2@test.com  ', ['test@test.com', 'test2@test.com']),
            ('test@test.com  , test2@test.com  ,', ['test@test.com', 'test2@test.com']),
        ]

        for test in tests:
            self.contact.form_email_address = test[0]
            self.assertEquals(self.contact._email_addresses(), test[1])
