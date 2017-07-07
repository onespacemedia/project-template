from django.apps import AppConfig
from watson import search as watson


class FaqsConfig(AppConfig):
    name = '{{ cookiecutter.package_name }}.apps.faqs'
    verbose_name = 'FAQ'
    verbose_name_plural = 'FAQs'

    def ready(self):
        from cms.models import PageBaseSearchAdapter

        Faq = self.get_model('Faq')
        watson.register(Faq, adapter_cls=PageBaseSearchAdapter)
