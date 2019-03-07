from django.contrib import admin

{% if cookiecutter.sections == 'yes' %}from ...utils.admin import UsedOnAdminMixin{% endif %}
from .models import CallToAction


@admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin{% if cookiecutter.sections == 'yes' %}, UsedOnAdminMixin{% endif %}):
    list_display = ['title'{% if cookiecutter.sections == 'yes' %}, 'pages_used_on'{% endif %}]
    fieldsets = (
        (None, {
            'fields': ['kicker', 'title', 'link_text', 'link_page', 'link_url']
        }),
    )
