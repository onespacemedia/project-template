from django_jinja import library

from ..models import Career


@library.global_function
def get_careers(count=3):
    """Renders the URL for the current article archive."""
    return Career.objects.all().select_open()[:count]
