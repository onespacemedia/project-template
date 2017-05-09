import json
import os

import jinja2
from cms.apps.pages.templatetags.pages import _navigation_entries
from django.conf import settings
from django.utils.safestring import mark_safe
from django_jinja import library
from sorl.thumbnail import get_thumbnail


@library.global_function
@jinja2.contextfunction
def get_navigation_json(context, pages, section=None):
    return json.dumps(_navigation_entries(context, pages, section, is_json=True))


@library.global_function
def frontend_templates():
    return mark_safe([
        str(f[:-5])
        for f in os.listdir(os.path.join(settings.TEMPLATES[0]['DIRS'][0], 'frontend'))
        if f[:1] != '_'
    ])


# Usage: get_next_by_field(obj, 'date')
@library.global_function
def get_next_by_field(obj, field):
    try:
        return getattr(obj, 'get_next_by_{}'.format(field))()
    except obj.DoesNotExist:
        return obj._default_manager.last()
    except Exception:
        pass  # Will cause 'None' to be returned.


# Usage: get_previous_by_field(obj, 'date')
@library.global_function
def get_previous_by_field(obj, field):
    try:
        return getattr(obj, 'get_previous_by_{}'.format(field))()
    except obj.DoesNotExist:
        return obj._default_manager.first()
    except Exception:
        pass  # Will cause 'None' to be returned.


@library.global_function
@library.render_with('images/lazy.html')
def lazy_image(image, height=None, width=None):
    """
    Usage: {{ lazy_image(path.to.image) }}
    
    :param image: 
    :param height: 
    :param width: 
    :return: 
    """

    # Ideally we will use the images uploaded sizes to get our aspect ratio but in certain circumstances, like cards,
    # we will use our own provided ones
    if not height:
        height = image.height

    if not width:
        width = image.width

    # The aspect ratio will be used to size the image with a padding-bottom based element
    aspect_ratio = '{}%'.format((height / width) * 100)
    small_image_url = get_thumbnail(image.file, str(int(width / 20))).url
    large_image_url = get_thumbnail(image.file, str(width)).url

    return {
        'aspect_ratio': aspect_ratio,
        'small_image_url': small_image_url,
        'large_image_url': large_image_url,
    }
