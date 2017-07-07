from .base import BaseRedirectTestCase


class RedirectTestCase(BaseRedirectTestCase):

    def test_unicode(self):
        # Make sure the __unicode__ method works fine.
        self.assertEqual(
            self.regex_redirect.__unicode__(),
            self.regex_redirect.old_path,
        )

    def test_sub_path(self):
        # Make sure the sub_path function is working for regular expression
        # redirects.
        self.assertEqual(
            self.regex_redirect.sub_path("/regex-tset-cases/regex-redirect/"),
            "/regex-test-cases/regex-redirect/",
        )

        # And make sure that it just returns the new path in the case that
        # a redirect is a non-regex one.
        self.assertEqual(
            self.normal_redirect.sub_path("/tset-cases/normal-redirect/"),
            "/test-cases/normal-redirect/",
        )
