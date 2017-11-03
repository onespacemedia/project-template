from cms.apps.pages.middleware import RequestPageManager
from cms.apps.pages.models import Page
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from watson import search

from ..admin import PersonAdmin
from ..models import Person
from ._base import PeopleBaseTestCase


class MockSuperUser(object):
    pk = 1

    def has_perm(self, perm):
        return True


class PeopleAdminFormTestCase(PeopleBaseTestCase):
    def setUp(self):
        super().setUp()
        self.site = AdminSite()
        self.admin = PersonAdmin(Person, self.site)
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.user = MockSuperUser()

    def test_form_clean_twitter(self):
        form = self.admin.get_form(self.request, obj=None)()
        form.cleaned_data = {}
        check_these = [
            'onespacemedia',
            '@onespacemedia',
            'https://twitter.com/onespacemedia',
            'https://m.twitter.com/onespacemedia',
            'twitter.com/onespacemedia',
        ]
        for check_this in check_these:
            form.cleaned_data['twitter'] = check_this
            self.assertEquals(form.clean_twitter(), 'onespacemedia')

    def test_form_clean_linkedin(self):
        form = self.admin.get_form(self.request, obj=None)()
        form.cleaned_data = {}
        check_these = [
            'onespacemedia',
            '@onespacemedia',
            'https://www.linkedin.com/in/onespacemedia',
            'www.linkedin.com/in/onespacemedia',
        ]
        for check_this in check_these:
            form.cleaned_data['linkedin'] = check_this
            self.assertEquals(form.clean_linkedin(), 'https://www.linkedin.com/in/onespacemedia')

    def test_form_get_form(self):
        # Ensure a default page is being set for new objects.
        form = self.admin.get_form(self.request, obj=None)()
        self.assertEquals(form.base_fields['page'].initial, self.person_page)
