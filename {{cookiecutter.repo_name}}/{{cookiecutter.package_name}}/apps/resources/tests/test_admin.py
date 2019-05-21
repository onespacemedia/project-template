from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory

from ..admin import ResourceAdmin
from ..models import Resource
from ._base import ResourcesBaseTestCase


class MockSuperUser(object):
    pk = 1

    def has_perm(self, perm):
        return True


class ResourcesAdminTestCase(ResourcesBaseTestCase):
    def setUp(self):
        super().setUp()
        self.site = AdminSite()
        self.admin = ResourceAdmin(Resource, self.site)
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.user = MockSuperUser()

    def test_resourceadmin_get_form(self):
        # Ensure a default page is being set for new objects.
        form = self.admin.get_form(self.request, obj=None)()
        self.assertEquals(form.base_fields['page'].initial, self.resources_page)
