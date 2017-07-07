from django.apps import AppConfig
from watson import search as watson


class EventsConfig(AppConfig):
    name = '{{ cookiecutter.package_name }}.apps.events'

    def ready(self):
        from cms.models import PageBaseSearchAdapter

        Event = self.get_model('Event')
        watson.register(Event, adapter_cls=PageBaseSearchAdapter)
