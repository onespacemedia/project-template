from django.conf import settings
from django.test import TestCase

from ..utils import url_from_path


class UtilsUtilsTest(TestCase):

    def test_url_from_path(self):

        site_url = url_from_path('\\')
        site_domain = settings.SITE_DOMAIN

        self.assertTrue(site_url.startswith('http'))
        self.assertIn(site_domain, site_url)
