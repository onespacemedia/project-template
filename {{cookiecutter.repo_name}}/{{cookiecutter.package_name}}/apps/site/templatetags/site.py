import json
import jinja2

from cms.apps.pages.templatetags.pages import _navigation_entries
from django_jinja import library


@library.global_function
@jinja2.contextfunction
def navigation_json(context, pages, section=None):
    return json.dumps(_navigation_entries(context, pages, section, is_json=True))
