import json
import os

import jinja2
from cms.apps.pages.templatetags.pages import _navigation_entries
from django.conf import settings
from django.utils.safestring import mark_safe
from django_jinja import library


@library.global_function
@jinja2.contextfunction
def get_navigation_json(context, pages, section=None):
    return json.dumps(_navigation_entries(context, pages, section, is_json=True))


@library.global_function
def frontend_templates():
    return mark_safe([
         str(f[:-5])
         for f in os.listdir(os.path.join(settings.TEMPLATES[0]["DIRS"][0], 'frontend'))
         if f[:1] != '_'
     ])
