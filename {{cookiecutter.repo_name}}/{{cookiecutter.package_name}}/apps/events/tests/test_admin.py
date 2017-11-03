from cms.admin import PageBaseAdmin
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory

from ..admin import EventAdmin
from ..models import Event
from ._base import EventsBaseTestCase


class MockSuperUser(object):
    pk = 1

    def has_perm(self, perm):
        return True


class EventsAdminTestCase(EventsBaseTestCase):
    def setUp(self):
        super().setUp()
        self.site = AdminSite()
        self.admin = EventAdmin(Event, self.site)
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.user = MockSuperUser()

    def test_eventadmin_fieldsets(self):
        # Make sure NAVIGATION_FIELDS aren't in the fieldsets, which are not
        # meaningful for a non-page object.
        self.assertNotIn(PageBaseAdmin.NAVIGATION_FIELDS, EventAdmin.fieldsets)

    def test_eventadmin_get_form(self):
        # Ensure a default page is being set for new objects.
        form = self.admin.get_form(self.request, obj=None)()
        self.assertEquals(form.base_fields['page'].initial, self.events_page)
