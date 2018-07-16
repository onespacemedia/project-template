import jinja2
from django import template
from django.core.cache import cache
from django.template.loader import render_to_string
from django_jinja import library

register = template.Library()


@library.global_function
@jinja2.contextfunction
def render_section(context, page_section):
    cached_content = cache.get(page_section.cache_key)
    request = context['request']

    if cached_content and not request.GET.get('cache_bypass') and not request.user.is_staff:
        return cached_content

    context = dict(context)
    context['section'] = page_section

    cached_content = render_to_string('sections/types/{}/{}'.format(
        page_section.template['folder'],
        page_section.template['file_name'],
    ), context)
    cache.set(page_section.cache_key, cached_content, 120)
    return cached_content
