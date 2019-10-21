from django.contrib import admin
from osm_jet.admin import JetCompactInline
from reversion.admin import VersionAdmin

from ...utils.admin import LinkFieldsLastAdminMixin{% if cookiecutter.sections == 'yes' %}, UsedOnAdminMixin{% endif %}
from .models import CallToAction, Link, LinkSet


@admin.register(CallToAction)
class CallToActionAdmin(LinkFieldsLastAdminMixin, admin.ModelAdmin{% if cookiecutter.sections == 'yes' %}, UsedOnAdminMixin{% endif %}):
    list_display = ['title'{% if cookiecutter.sections == 'yes' %}, 'pages_used_on'{% endif %}]


class LinkAdmin(JetCompactInline):
    model = Link
    extra = 0


@admin.register(LinkSet)
class LinkSetAdmin(VersionAdmin{% if cookiecutter.sections == 'yes' %}, UsedOnAdminMixin{% endif %}):
    list_display = ['__str__'{% if cookiecutter.sections == 'yes' %}, 'pages_used_on'{% endif %}]
    inlines = [LinkAdmin]
