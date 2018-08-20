from adminsortable2.admin import SortableAdminMixin
from cms.admin import PageBaseAdmin
from django.contrib import admin

from .models import Partner


@admin.register(Partner)
class PartnerAdmin(SortableAdminMixin, PageBaseAdmin):
    list_display = ['order', 'title', 'is_online']
    list_editable = ['is_online']

    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'logo'],
        }),
        ('Content', {
            'fields': ['summary', 'website'],
        }),
        PageBaseAdmin.PUBLICATION_FIELDS,
        PageBaseAdmin.NAVIGATION_FIELDS,
        PageBaseAdmin.SEO_FIELDS,
        PageBaseAdmin.OPENGRAPH_FIELDS,
        PageBaseAdmin.OPENGRAPH_TWITTER_FIELDS,
    ]
