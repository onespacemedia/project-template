import re

from django import http
from django.conf import settings
from django.shortcuts import redirect

from .models import Redirect


class RedirectFallbackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # No need to check for a redirect for non-404 responses.
        if response.status_code != 404:
            return response

        path = request.get_full_path()
        r = self._redirect_for_path(path)

        # Try removing or adding the trailing slash.
        if r is None:
            if path.endswith('/'):
                r = self._redirect_for_path(path[:-1])
            else:
                r = self._redirect_for_path('{}/'.format(path))

        if r is not None:
            if r.new_path == '':
                return http.HttpResponseGone()
            return redirect(r.sub_path(path), permanent=r.type == '301')

        return response

    def _redirect_for_path(self, path):
        try:
            return Redirect.objects.get(old_path=path)
        except Redirect.DoesNotExist:
            pass

        if getattr(settings, "REDIRECTS_ENABLE_REGEX", False):
            for obj in Redirect.objects.all():
                if obj.regular_expression and re.match(obj.old_path, path):
                    return redirect

        return None
