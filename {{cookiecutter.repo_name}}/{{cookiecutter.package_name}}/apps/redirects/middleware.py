import re
{% if cookiecutter.multilingual == 'yes' %}
from cms.apps.pages.models import Country
{% endif %}from django import http
from django.conf import settings{% if cookiecutter.multilingual == 'yes' %}

from ...utils.utils import get_country_code{% endif %}

from .models import Redirect


class RedirectFallbackMiddleware:
    def _redirect_for_path(self, path):
        if not getattr(settings, "REDIRECTS_ENABLE_REGEX", False):
            try:
                return Redirect.objects.get(old_path=path)
            except Redirect.DoesNotExist:
                return None

        for redirect in Redirect.objects.all():
            if redirect.old_path == path:
                return redirect
            if redirect.regular_expression and re.match(redirect.old_path, path):
                return redirect

        return None

    def process_response(self, request, response):
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
                r = self._redirect_for_path(f'{path}/')

        if r is not None:
            if r.new_path == '':
                return http.HttpResponseGone()
            new_path = r.sub_path(path)
            {% if cookiecutter.multilingual == 'yes' %}
            existing_code = re.match(r'/([^/]*)/', r.new_path)
            if not (existing_code and Country.objects.filter(code=existing_code.group(1)).exists()):
                new_path = f'/{get_country_code()}{new_path}'
            {% endif %}
            return http.HttpResponsePermanentRedirect(new_path) if r.type == '301' else http.HttpResponseRedirect(new_path)

        # No redirect was found. Return the response.
        return response
