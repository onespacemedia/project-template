from django.apps import AppConfig
from watson import search as watson


class PartnersConfig(AppConfig):
    name = '{{ project_name }}.apps.partners'

    def ready(self):
        from cms.models import PageBaseSearchAdapter

        Partner = self.get_model('Partner')
        watson.register(Partner, adapter_cls=PageBaseSearchAdapter)
