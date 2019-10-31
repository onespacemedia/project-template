from django.test import Client, TestCase
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_password_reset_view(self):
        response = self.client.get(reverse('password_reset'))
        self.assertTemplateUsed(response, 'users/reset/password_reset_form.html')

    def test_password_reset_done_view(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertTemplateUsed(response, 'users/reset/password_reset_done.html')

    def test_password_reset_complete_view(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertTemplateUsed(response, 'users/reset/password_reset_complete.html')
