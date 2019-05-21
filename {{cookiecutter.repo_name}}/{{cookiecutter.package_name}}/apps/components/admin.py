from django.contrib import admin

from ...utils.admin import LinkFieldsLastAdminMixin{% if cookiecutter.sections == 'yes' %}, UsedOnAdminMixin{% endif %}
from .models import CallToAction


@admin.register(CallToAction)
class CallToActionAdmin(LinkFieldsLastAdminMixin, admin.ModelAdmin{% if cookiecutter.sections == 'yes' %}, UsedOnAdminMixin{% endif %}):
    list_display = ['title'{% if cookiecutter.sections == 'yes' %}, 'pages_used_on'{% endif %}]
