from cms.admin import PageBaseAdmin
from django.contrib import admin
from suit.admin import SortableModelAdmin

from .models import Partner


@admin.register(Partner)
class PartnerAdmin(SortableModelAdmin, PageBaseAdmin):
    list_display = ['title', 'is_online', 'order']
    list_editable = ['is_online', 'order']

    fieldsets = [
        (None, {
            'fields': ['page', 'title', 'slug'],
        }),
        ('Content', {
            'fields': ['summary', 'logo', 'website'],
        }),
        PageBaseAdmin.PUBLICATION_FIELDS,
        PageBaseAdmin.NAVIGATION_FIELDS,
        PageBaseAdmin.SEO_FIELDS,
        PageBaseAdmin.OPENGRAPH_FIELDS,
        PageBaseAdmin.OPENGRAPH_TWITTER_FIELDS,
    ]

