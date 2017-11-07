from importlib import reload

from django.test import TestCase

from .. import admin


class AdminTestCase(TestCase):
    def test_admin_unregistering_no_exception(self):
        reload(admin)
