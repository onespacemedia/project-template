import hashlib
import os
import urllib

import CommonMark
import jinja2
from bs4 import BeautifulSoup
from cms.apps.pages.templatetags.pages import _navigation_entries
from cms.html import process as process_html
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.urls import NoReverseMatch, reverse
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


@library.filter
@stringfilter
def html(text):
    # Return empty string if no text
    if not text:
        return ""

    # Process HTML through cms parser
    text = process_html(text)

    # Load text into BS4
    soup = BeautifulSoup(text, 'html.parser')

    # Unwrap all image tags
    for img in soup.find_all('img'):
        if not img.parent.has_attr('class'):
            img.parent.unwrap()

    def wrap(to_wrap, wrap_in):
        contents = to_wrap.replace_with(wrap_in)
        wrap_in.append(contents)

    # Wrap all table tags
    for table in soup.find_all('table'):
        div = soup.new_tag('div')
        div['class'] = 'wys-TableWrap'
        wrap(table, div)

    # Wrap all iframes in intrinsic containers
    for iframe in soup.find_all('iframe'):
        for attr in ['width', 'height']:
            if iframe.get(attr, None):
                del iframe[attr]
        wrapper = soup.new_tag('div', **{'class': 'wys-Intrinsic'})
        iframe.wrap(wrapper)

    # Force return string version of BS4 obj
    return mark_safe(str(soup))


@library.global_function
def get_header_content():
    return Header.objects.first()


@library.global_function
def get_footer_content():
    return Footer.objects.first()


@library.global_function
@library.render_with('edit_bar.html')
@jinja2.contextfunction
def edit_bar(context):
    context = dict(context)
    request = context['request']

    # Don't show to non-admins, and don't pretend that /search/ is editable.
    if not request.user.is_staff or request.path == '/search/':
        context['show'] = False
        return context

    obj = context.get('object')

    if obj:
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name

        if request.user.has_perm(f'{app_label}.change_{model_name}'):
            try:
                add_url = reverse(f'admin:{app_label}_{model_name}_add')
                edit_url = reverse(f'admin:{app_label}_{model_name}_change', args=[obj.pk])

                context.update({
                    'add_url': add_url,
                    'edit_url': edit_url,
                    'model_name': obj._meta.verbose_name,
                    'show': True,
                })
                return context

            except NoReverseMatch:
                context['show'] = False
                return context
        else:
            context['show'] = False
            return context

    elif 'pages' in context and context['pages'].current and request.user.has_perm('pages.change_page'):
        context.update({
            'add_url': reverse('admin:pages_page_add'),
            'edit_url': reverse('admin:pages_page_change', args=[context['pages'].current.pk]),
            'model_name': 'page',
            'show': True,
        })
        return context

    context['show'] = False
    return context


@library.global_function
def gravatar_url(email, size=40):
    return "https://www.gravatar.com/avatar/{}?{}".format(
        hashlib.md5(email.lower().encode('utf-8')).hexdigest(),
        urllib.parse.urlencode({
            'd': 'mm',
            's': str(size)
        })
    )
