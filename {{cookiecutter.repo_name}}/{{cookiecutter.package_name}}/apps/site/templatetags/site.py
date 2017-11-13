import os

import CommonMark
import jinja2
from cms.apps.pages.templatetags.pages import _navigation_entries
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django_jinja import library
from sorl.thumbnail import get_thumbnail

from ..models import Footer, Header


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
@library.render_with('pages/navigation.html')
@jinja2.contextfunction
def render_navigation(context, pages, section=None, recursive=False):
    """
    Renders a navigation list for the given pages.

    The pages should all be a subclass of PageBase, and possess a get_absolute_url() method.

    You can also specify an alias for the navigation, at which point it will be set in the
    context rather than rendered.
    """
    return {
        'navigation': _navigation_entries(context, pages, section),
        'recursive': recursive,
    }


@library.global_function
def lazy_image(image, height=None, width=None, blur=True, max_width=1920, crop=None):  # pylint: disable=too-many-arguments
    user_sized = height and width

    if user_sized and not crop:
        crop = 'center'

    # Ideally we will use the images uploaded sizes to get our aspect ratio but in certain circumstances, like cards,
    # we will use our own provided ones
    if not height:
        height = image.height

    if not width:
        width = image.width

    aspect_ratio = height / width if user_sized else image.height / image.width

    if width > max_width:
        width = max_width

    if width > height:
        height = int(width * aspect_ratio)

    # The aspect ratio will be used to size the image with a padding-bottom based element
    aspect_ratio_percentage = '{}%'.format(aspect_ratio * 100)

    original_large_image_url = reverse('assets:thumbnail', kwargs={
        'pk': image.pk,
        'width': width,
        'height': height,
        'format': 'source',
        'crop': crop,
    })

    original_large_image_url_2x = reverse('assets:thumbnail', kwargs={
        'pk': image.pk,
        'width': width * 2,
        'height': height * 2,
        'format': 'source',
        'crop': crop,
    })

    webp_url = reverse('assets:thumbnail', kwargs={
        'pk': image.pk,
        'width': width,
        'height': height,
        'format': 'webp',
        'crop': crop,
        # quality=80
    })

    webp_url_2x = reverse('assets:thumbnail', kwargs={
        'pk': image.pk,
        'width': width * 2,
        'height': height * 2,
        'format': 'webp',
        'crop': crop,
        # quality=80
    })

    try:
        small_image_url = get_thumbnail(image.file, str(int(width / 20))).url
    except ValueError:
        # Guard against really tiny images, i.e. width / 20 results in 0.
        small_image_url = original_large_image_url

    return {
        'alt_text': image.alt_text or '',
        'aspect_ratio': aspect_ratio_percentage,
        'small_image_url': small_image_url,
        'original_large_image_url': original_large_image_url,
        'original_large_image_url_2x': original_large_image_url_2x,
        'webp_url': webp_url,
        'webp_url_2x': webp_url_2x,
        'blur': blur
    }


@library.global_function
@library.render_with('images/lazy.html')
def render_lazy_image(image, height=None, width=None, blur=True, max_width=1920, crop=None):  # pylint: disable=too-many-arguments
    """
        Usage: {% raw %}{{ lazy_image(path.to.image) }}{% endraw %}
        :param crop:
        :param max_width:
        :param blur:
        :param image:
        :param height:
        :param width
        :return:
    """

    return lazy_image(image, height, width, blur, max_width, crop)


@library.filter
def md_escaped(value, inline=True):
    if not value:
        return ""

    formatted = value.strip()

    if inline:
        formatted = formatted.replace('\n', '<br>')

    formatted = CommonMark.commonmark(formatted).strip()

    # Remove wrapping <p> tags.
    if inline and formatted.startswith('<p>') and formatted.endswith('</p>'):
        formatted = formatted[3:-4]

    return formatted


@library.filter
def md(value, inline=True):
    """
    Formats a string of Markdown text to HTML.

    By default it assumes that the text will be wrapped in a meaningful
    block-level element, i.e. the return value will not be wrapped in a `<p>`
    tag, and line breaks will be rendered using `<br>` elements. If you wish
    to override this and use standard Markdown behaviour, pass `inline=True`
    as an argument to this filter.

    This should never be used on untrusted user input, as Markdown by design
    allows arbitrary HTML.
    """
    return mark_safe(md_escaped(value, inline=inline))


@library.global_function
def get_header_content():
    return Header.objects.first()


@library.global_function
def get_footer_content():
    return Footer.objects.first()
