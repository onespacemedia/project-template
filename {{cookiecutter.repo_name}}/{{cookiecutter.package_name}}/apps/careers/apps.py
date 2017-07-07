from django.apps import AppConfig
from watson import search as watson


class CareersConfig(AppConfig):
    name = '{{ project_name }}.apps.careers'

    def ready(self):
        from cms.models import PageBaseSearchAdapter

        Career = self.get_model('Career')
        watson.register(Career, adapter_cls=PageBaseSearchAdapter)
