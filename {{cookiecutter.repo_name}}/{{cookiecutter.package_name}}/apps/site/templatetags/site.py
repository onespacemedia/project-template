import json
import os

import jinja2
from cms.apps.pages.templatetags.pages import _navigation_entries
from django.conf import settings
from django.utils.safestring import mark_safe
from django_jinja import library
from sorl.thumbnail import get_thumbnail

# from ..models import Footer, Header


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
    except Exception:  # pylint:disable=broad-except
        pass  # Will cause 'None' to be returned.


# Usage: get_previous_by_field(obj, 'date')
@library.global_function
def get_previous_by_field(obj, field):
    try:
        return getattr(obj, 'get_previous_by_{}'.format(field))()
    except obj.DoesNotExist:
        return obj._default_manager.first()
    except Exception:  # pylint:disable=broad-except
        pass  # Will cause 'None' to be returned.


@library.global_function
def lazy_image(image, height=None, width=None, blur=True, max_width=1920, crop=None):  # pylint: disable=too-many-arguments
    # Ideally we will use the images uploaded sizes to get our aspect ratio but in certain circumstances, like cards,
    # we will use our own provided ones
    if not height:
        height = image.height

    if not width:
        width = image.width

    aspect_ratio = height / width

    if width > max_width:
        width = max_width

    # The aspect ratio will be used to size the image with a padding-bottom based element
    aspect_ratio_percentage = '{}%'.format(aspect_ratio * 100)
    small_image_url = get_thumbnail(image.file, str(int(width / 20))).url
    large_image_url = get_thumbnail(image.file, f'{width}x{height}', crop=crop).url
    large_image_url_2x = get_thumbnail(image.file, f'{width * 2}x{height * 2}', crop=crop).url

    return {
        'alt_text': image.alt_text or '',
        'aspect_ratio': aspect_ratio_percentage,
        'small_image_url': small_image_url,
        'large_image_url': large_image_url,
        'large_image_url_2x': large_image_url_2x,
        'blur': blur
    }


@library.global_function
@library.render_with('images/lazy.html')
def render_lazy_image(image, height=None, width=None, blur=True, max_width=1920, crop=None):  # pylint: disable=too-many-arguments
    """
        Usage: {{ lazy_image(path.to.image) }}
        :param crop:
        :param max_width:
        :param blur:
        :param image:
        :param height:
        :param width
        :return:
    """

    return lazy_image(image, height, width, blur, max_width, crop)


@library.global_function
def get_header_content():
    try:
        return Header.objects.first()
    except IndexError:
        return None


@library.global_function
def get_footer_content():
    try:
        return Footer.objects.first()
    except IndexError:
        return None
