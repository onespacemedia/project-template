import errno

import jinja2
from django import template
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django_jinja import library

register = template.Library()


@library.global_function
@jinja2.contextfunction
def render_section(context, page_section):
    try:
        context = dict(context)
        context['section'] = page_section

        return render_to_string(f'sections/types/{page_section.template["folder"]}/{page_section.template["file_name"]}', context)
    except TemplateDoesNotExist as e:
        import os
        from django.conf import settings

        if settings.DEBUG:
            try:
                os.makedirs(f'example_project/apps/sections/templates/sections/types/{page_section.template["folder"]}')
            except OSError as exc:  # Python >2.5
                if exc.errno == errno.EEXIST and os.path.isdir(page_section.template["folder"]):
                    pass
                else:
                    raise

            os.system(f'touch example_project/apps/sections/templates/sections/types/{page_section.template["folder"]}/{page_section.template["file_name"]}')

            return ''
        else:
            raise e
