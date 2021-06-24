import jinja2
from django import template
from django.core.cache import cache
from django.template.loader import render_to_string
from django_jinja import library

from ..models import SECTION_TYPES

register = template.Library()


@library.global_function
@jinja2.contextfunction
def render_section(context, page_section):
    cached_content = cache.get(page_section.cache_key)
    request = context['request']

    if cached_content and page_section.cacheable and not (request.GET.get('cache_bypass') or request.user.is_staff):
        return cached_content

    context = dict(context)
    context['section'] = page_section

    cached_content = render_to_string(page_section.template_path, context)
    cache.set(page_section.cache_key, cached_content, 120)

    return cached_content


@library.global_function
@jinja2.contextfunction
@library.render_with('sections/includes/js.html')
def sections_js(context):
    pages = context['pages']
    sections = pages.current.contentsection_set.all()
    sections_with_js = {section_type['slug']: section_type['directory_name'] for section_type in SECTION_TYPES if section_type['javascript']}

    return {
        'entries': list({sections_with_js[section.type] for section in sections if section.type in sections_with_js})
    }
