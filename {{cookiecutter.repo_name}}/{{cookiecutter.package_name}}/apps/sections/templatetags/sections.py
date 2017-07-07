import jinja2
from django import template
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django_jinja import library

from ..models import get_section_name as get_section_name_base
from ..models import SECTION_TYPES

register = template.Library()


@library.global_function
@jinja2.contextfunction
def render_section(context, page_section):
    try:
        context = dict(context)
        context['section'] = page_section

        return render_to_string('sections/types/{}'.format(page_section.template), context)
    except TemplateDoesNotExist as e:
        import os
        from django.conf import settings

        if settings.DEBUG:
            os.system(f'touch {{ project_name }}/apps/sections/templates/sections/types/{page_section.template}')

            return ''
        else:
            raise e


@library.global_function
@jinja2.contextfunction
def section_contains_image(context, section_obj):
    if not section_obj.content_left or not section_obj.content_right:
        return ''

    if any('<img' in s for s in[section_obj.content_left, section_obj.content_right]):
        return 'has-media'

    return ''


@register.inclusion_tag('admin/pages/page/type_modal.html')
def render_type_modal():
    return {
        'section_types': SECTION_TYPES
    }


@register.simple_tag
def get_section_name(obj):
    if isinstance(obj, tuple):
        return get_section_name_base(obj)

    # We have the section type as a string.
    for _, sections in SECTION_TYPES:
        for section in sections['sections']:
            if section[0] == obj:
                return get_section_name_base(section)
