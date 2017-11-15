from django.contrib import admin

from .models import CallToAction
{% if cookiecutter.sections == 'yes' %}from ...utils.admin import UsedOnAdminMixin{% endif %}


@admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin{% if cookiecutter.sections == 'yes' %}, UsedOnAdminMixin{% endif %}):
    list_display = ['title'{% if cookiecutter.sections == 'yes' %}, 'pages_used_on'{% endif %}]
