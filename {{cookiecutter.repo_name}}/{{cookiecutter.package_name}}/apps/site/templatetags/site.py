import hashlib
import os
import urllib

import CommonMark
import jinja2
from bs4 import BeautifulSoup
from cms.apps.pages.templatetags.pages import _navigation_entries
from cms.html import process as process_html
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe
from django_jinja import library
from sorl.thumbnail import get_thumbnail
from webpack_loader.utils import get_files

from ..models import Footer, Header

register = template.Library()


@library.global_function
def path_to_url(path):
    if path.startswith('http://') or path.startswith('https://'):
        return path

    if not path.startswith('/'):
        path = '/' + path

    return u'https://{}{}{}'.format(
        'www.' if settings.PREPEND_WWW else '',
        settings.SITE_DOMAIN,
        path,
    )


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
    # Take a copy of the current context and update it - we do this so that
    # we have access to 'request', 'settings', etc.
    context = dict(context)
    context.update({
        'navigation': _navigation_entries(context, pages, section),
        'recursive': recursive,
    })
    return context


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


@register.simple_tag
@library.filter
def add_field_attributes(field, class_name, placeholder=True):
    return field.as_widget(attrs={
        'class': ' '.join((field.css_classes(), class_name)),
        'placeholder': field.label if placeholder else '',
    })


@library.global_function
@library.render_with('pagination/pagination.html')
@jinja2.contextfunction
def render_pagination(context, page_obj, offset=2, pagination_key=None):
    ''' Renders the pagination for the given page of items. Any items that are further than OFFSET
    from the current page are truncated except for the first and last pages which are always visible. '''
    current_page = page_obj.number

    page_range = page_obj.paginator.page_range

    offset_indexes = [
        x for x in range(current_page - offset, current_page + (offset + 1))
        if x >= 1
    ]

    # Always show the first page.
    if not 1 in offset_indexes:
        offset_indexes = [1] + offset_indexes

    # Always show the last page.
    if not len(page_range) in offset_indexes:
        offset_indexes = offset_indexes + [len(page_range)]

    page_numbers_adjusted = []

    # Ensure we don't get more than one ellipsed entry in a row.
    add_ellipses = False

    if len(page_range) > offset:
        for page in page_range:
            if (
                    page in offset_indexes
                    # Don't be like "[1] [..] [3] [4] [5]"
                    or (page == offset and current_page - page - offset == 1)
                    # Don't be like "[26] [27] [..] [29]"
                    or (
                        page == (len(page_range) - offset + 1)
                        and current_page + offset + 1 == len(page_range) - 1
                    )
            ):
                page_numbers_adjusted.append(page)
                add_ellipses = True
            elif add_ellipses:
                page_numbers_adjusted.append(None)
                add_ellipses = False
    else:
        page_numbers_adjusted = page_range

    return {
        'request': context['request'],
        'offset_indexes': offset_indexes,
        'offset': offset,
        'page_obj': page_obj,
        'page_numbers_adjusted': page_numbers_adjusted,
        'paginator': page_obj.paginator,
        'pagination_key': pagination_key or getattr(page_obj, '_pagination_key', 'page')
    }


@library.global_function
@library.render_with('_image_sourceset.html')
def render_2x_image(image, width='', height='', **kwargs):
    dimentions = f'{width}x{height}'
    width_2x = width * 2 if width else ''
    height_2x = height * 2 if height else ''
    dimentions_2x = f'{width_2x}x{height_2x}'

    image_url = get_thumbnail(image.file, dimentions, quality=100, **kwargs).url

    image_url_2x = get_thumbnail(image.file, dimentions_2x, quality=100, **kwargs).url

    webp_url = get_thumbnail(image.file, dimentions, quality=100, format='WEBP', **kwargs).url

    webp_url_2x = get_thumbnail(image.file, dimentions_2x, quality=100, format='WEBP', **kwargs).url

    return {
        'image': image_url,
        'image_2x': image_url_2x,
        'webp': webp_url,
        'webp_2x': webp_url_2x,
    }


@library.global_function
def get_css_path(bundle):
    return get_files(bundle, 'css')[0]['publicPath']
