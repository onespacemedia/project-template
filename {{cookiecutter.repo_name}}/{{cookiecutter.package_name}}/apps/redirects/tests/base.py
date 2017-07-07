from django.test import TestCase

from ..models import Redirect


class BaseRedirectTestCase(TestCase):
    def setUp(self):
        # A regular expression redirect.
        self.regex_redirect = Redirect.objects.create(
            old_path=r"/regex-tset-cases/(.*)/",
            new_path=r"/regex-test-cases/\1/",
            test_path=r"/regex-tset-cases/regex-redirect/",
            regular_expression=True,
        )

        # A normal non-regex redirect.
        self.normal_redirect = Redirect.objects.create(
            old_path=r"/tset-cases/normal-redirect/",
            new_path=r"/test-cases/normal-redirect/",
            regular_expression=False,
        )

        # A redirect that should return a 410 Gone.
        self.dead_redirect = Redirect.objects.create(
            old_path="/tset-cases/dead-redirect/",
            new_path="",
            regular_expression=False,
        )

        # A redirect to test
        self.unslashed_redirect = Redirect.objects.create(
            old_path="/tset-cases/unslashed-redirect",
            new_path="/test-cases/unslashed-redirect/",
            regular_expression=False,
        )
