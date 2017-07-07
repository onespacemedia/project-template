from django.apps import AppConfig
from watson import search as watson


class PeopleConfig(AppConfig):
    name = '{{ cookiecutter.package_name }}.apps.people'

    def ready(self):
        from cms.models import PageBaseSearchAdapter

        Person = self.get_model('Person')
        watson.register(Person, adapter_cls=PageBaseSearchAdapter)
