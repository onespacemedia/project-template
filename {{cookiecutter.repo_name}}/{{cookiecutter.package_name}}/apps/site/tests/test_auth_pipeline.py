from django.http import HttpResponse
from django.test import TestCase

from ..auth_pipeline import make_staff


class Backend:
    name = None

    def __init__(self, name, *args, **kwargs):
        super(Backend, self).__init__(*args, **kwargs)
        self.name = name


class MockSuperUser:
    is_staff = False
    is_superuser = False

    def save(self):
        pass


class PipelineTest(TestCase):

    def test_make_staff(self):
        facebook_backend = Backend('facebook')
        google_oauth2_backend = Backend('google-oauth2')
        user = MockSuperUser()
        response = HttpResponse()

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        make_staff(facebook_backend, user, response)

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        make_staff(google_oauth2_backend, user, response)

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
