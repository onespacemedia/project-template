from django.conf import settings
from django.template.loader import render_to_string
from django.test import TestCase


class TestEmails(TestCase):
    def test_password_reset_html(self):
        email = render_to_string(
            'emails/password_reset.html',
            context={
                'user': {
                    'first_name': 'Test'
                },
                'settings': settings,
                'protocol': 'https',
                'domain': settings.SITE_DOMAIN,
                'uid': 'aa',
                'token': 'test-token',
            }
        )

        self.assertIn(f'href="https://{settings.SITE_DOMAIN}/admin/reset-password/reset/aa/test-token/"', email)

    def test_password_reset_text(self):
        email = render_to_string(
            'emails/password_reset.txt',
            context={
                'settings': settings,
                'protocol': 'https',
                'domain': settings.SITE_DOMAIN,
                'uid': 'aa',
                'token': 'test-token',
            }
        )

        self.assertIn(f'https://{settings.SITE_DOMAIN}/admin/reset-password/reset/aa/test-token/', email)
