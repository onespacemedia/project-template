from django.http import HttpResponse, HttpResponseNotFound
from django.test import RequestFactory

from ..middleware import RedirectFallbackMiddleware
from ..models import Redirect
from .base import BaseRedirectTestCase


class RedirectMiddlewareTestCase(BaseRedirectTestCase):
    def setUp(self):
        super(RedirectMiddlewareTestCase, self).setUp()
        self.factory = RequestFactory()

    def test_redirect_for_path(self):
        # If regex redirects are disabled, then ensure that the redirect does
        # what it says on the tin.
        with self.settings(REDIRECTS_ENABLE_REGEX=False):
            middleware = RedirectFallbackMiddleware()

            middleware.process_response(
                self.factory.get(self.normal_redirect.old_path),
                HttpResponseNotFound()
            )

            self.assertEqual(
                middleware._redirect_for_path(self.normal_redirect.old_path).new_path,
                self.normal_redirect.new_path
            )

        # If regex redirects are enabled, then make sure that 1) if a path is
        # an exact match for a redirect, that it will return the redirect with
        # an exact match 2) that if there is a regex redirect that matches it,
        # that it will return that one, and 3) that if there's no matching
        # path, that it returns None.
        with self.settings(REDIRECTS_ENABLE_REGEX=True):
            middleware = RedirectFallbackMiddleware()

            self.assertEqual(
                middleware._redirect_for_path(self.normal_redirect.old_path),
                self.normal_redirect
            )

            self.assertEqual(
                middleware._redirect_for_path(self.regex_redirect.old_path),
                self.regex_redirect
            )

            self.assertEqual(
                middleware._redirect_for_path("/make-it-return-None/"),
                None
            )

    def test_process_response(self):
        # Make sure that non-404 responses are not processed.
        middleware = RedirectFallbackMiddleware()

        response = middleware.process_response(
            self.factory.get("/"),
            HttpResponse()
        )

        self.assertEqual(response.status_code, 200)

        # Test that a redirect with an empty new_path returns a 410 Gone.
        response = middleware.process_response(
            self.factory.get(self.dead_redirect.old_path),
            HttpResponseNotFound
        )

        self.assertEqual(response.status_code, 410)

        # Test that a redirect has the appropriate status code and Location
        # header.
        response = middleware.process_response(
            self.factory.get(self.normal_redirect.old_path),
            HttpResponseNotFound
        )

        self.assertEqual(self.normal_redirect.new_path, response["Location"])
        self.assertEqual(response.status_code, 301)

        # Test that a request to a completely imaginary path that doesn't
        # have a redirect will 404.
        response = middleware.process_response(
            self.factory.get("/if-this-doesnt-404-i-broke-it/"),
            HttpResponseNotFound
        )
        self.assertEqual(response.status_code, 404)

        # Make sure that old paths missing a trailing forward slash are
        # redirected appropriately.
        response = middleware.process_response(
            self.factory.get(self.unslashed_redirect.old_path),
            HttpResponseNotFound
        )

        self.assertEqual(
            self.unslashed_redirect.new_path,
            response["Location"]
        )
