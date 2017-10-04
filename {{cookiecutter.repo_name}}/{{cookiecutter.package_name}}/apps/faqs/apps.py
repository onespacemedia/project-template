from django.apps import AppConfig


class FaqsConfig(AppConfig):
    name = '{{ cookiecutter.package_name }}.apps.faqs'
    verbose_name = 'FAQ'
    verbose_name_plural = 'FAQs'
