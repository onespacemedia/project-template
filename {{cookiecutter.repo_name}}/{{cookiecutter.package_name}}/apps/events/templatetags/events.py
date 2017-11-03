from django_jinja import library

from ..models import Event, Events


@library.global_function
def get_events_list_url():
    """Renders the URL for the current article archive."""
    return Events.objects.all()[0].page.get_absolute_url()


@library.global_function
def get_upcoming_events(count=3):
    return Event.objects.select_upcoming().order_by('end_date')[:count]
