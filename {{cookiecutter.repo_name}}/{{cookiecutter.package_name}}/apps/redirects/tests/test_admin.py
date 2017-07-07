from django.contrib.admin.sites import AdminSite, NotRegistered
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import RequestFactory

from ...redirects import admin
from ..admin import RedirectModelForm
from ..models import Redirect
from .base import BaseRedirectTestCase


class RedirectAdminTestCase(BaseRedirectTestCase):
    def setUp(self):
        super(RedirectAdminTestCase, self).setUp()
        self.site = None
        self.reset_admin()
        self.admin_user = get_user_model().objects.create_superuser(
            username="unittesting",
            email="lewis.collard@onespacemedia.com",
            password="lewis",
        )

    def reset_admin(self):
        if self.site:
            try:
                self.site.unregister(Redirect)
            except NotRegistered:
                pass
        self.site = AdminSite()
        self.admin = admin.RedirectAdmin(Redirect, self.site)

    def test_get_list_display(self):
        # Test that list_display is set properly when regex redirects are
        # disabled.
        request = RequestFactory().get(reverse("admin:redirects_redirect_changelist"))
        with self.settings(REDIRECTS_ENABLE_REGEX=False):
            self.reset_admin()
            self.assertEqual(
                self.admin.get_list_display(request),
                ('old_path', 'new_path', 'test_redirect')
            )

        with self.settings(REDIRECTS_ENABLE_REGEX=True):
            self.reset_admin()
            self.assertEqual(
                self.admin.get_list_display(request),
                ('old_path', 'new_path', 'regular_expression', 'test_redirect')
            )

    def test_get_form(self):
        # form = self.admin.get_form()
        request = RequestFactory().get(reverse("admin:redirects_redirect_changelist"))

        # Make sure nothing is broken depending on REDIRECTS_ENABLE_REGEX
        # setting.
        with self.settings(REDIRECTS_ENABLE_REGEX=True):
            self.admin.get_form(request)

        with self.settings(REDIRECTS_ENABLE_REGEX=False):
            self.admin.get_form(request)

    def test_test_redirect(self):
        # Ensure that the 'test redirect' pseudo-column has not broken.
        column = self.admin.test_redirect(self.normal_redirect)
        self.assertEqual(
            column,
            '<a target="_blank" href="{}">Test</a>'.format(self.normal_redirect.old_path)
        )

    def test_form(self):
        # Test for invalid from_path.
        form = RedirectModelForm({
            "old_path": "invalid",
            "new_path": "/",
            "regular_expression": False,
        })

        self.assertFalse(form.is_valid())

        # Test a valid non-regex redirect.
        form = RedirectModelForm({
            "old_path": "/good/",
            "new_path": "/",
            "regular_expression": False,
        })

        self.assertTrue(form.is_valid())

        with self.settings(REDIRECTS_ENABLE_REGEX=True):
            # Test for a missing 'test_path' attribute from a regex
            form = RedirectModelForm({
                "old_path": "/broken/",
                "new_path": "/",
                "regular_expression": True,
            })
            self.assertFalse(
                form.is_valid(),
            )

            # Test for a broken regex in from path.
            form = RedirectModelForm({
                "old_path": "/old-path/(.*)(/",
                "new_path": "/new-path/",
                "regular_expression": True,
                "test_path": "/old-path/test-me/"
            })

            self.assertFalse(
                form.is_valid(),
            )
