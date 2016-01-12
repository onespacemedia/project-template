import json

from django import template

register = template.Library()


@register.filter
def here(page, request):
    return request.path.startswith(page.get_absolute_url())


@register.simple_tag
def node_module(path):
    return '/node_modules/{}'.format(path)


@register.assignment_tag(takes_context=True)
def navigation_json(context, pages, section=None):
    """
    Renders a navigation list for the given pages.

    The pages should all be a subclass of PageBase, and possess a get_absolute_url() method.

    You can also specify an alias for the navigation, at which point it will be set in the
    context rather than rendered.
    """
    request = context["request"]

    # Compile the entries.
    def page_entry(page):
        # Do nothing if the page is to be hidden from not logged in users
        if page.hide_from_anonymous and not request.user.is_authenticated():
            return

        # Do nothing if the page is set to offline
        if not page.is_online:
            return

        url = page.get_absolute_url()

        return {
            "url": url,
            "title": str(page),
            "here": request.path.startswith(url),
            "children": [page_entry(x) for x in page.navigation if
                         page is not request.pages.homepage]
        }

    # All the applicable nav items
    entries = [page_entry(x) for x in pages if page_entry(x) is not None]

    # Add the section.
    if section:
        section_entry = page_entry(section)
        entries = [section_entry] + list(entries)

    return json.dumps(entries)
