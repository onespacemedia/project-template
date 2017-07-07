from django_jinja import library

from ..models import Events


@library.global_function
def get_events_list_url():
    """Renders the URL for the current article archive."""
    return Events.objects.all()[0].page.get_absolute_url()
