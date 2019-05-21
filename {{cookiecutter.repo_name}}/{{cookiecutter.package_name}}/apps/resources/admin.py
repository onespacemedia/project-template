from cms.admin import OnlineBaseAdmin, PageBaseAdmin
from django.contrib import admin
from reversion.admin import VersionAdmin
from reversion.models import Version

from ...utils.admin import HasImageAdminMixin
from .models import Resource, Resources, ResourceType


@admin.register(ResourceType)
class ResourceTypeAdmin(VersionAdmin):
    list_display = ['__str__']
    prepopulated_fields = {'slug': ['title']}


@admin.register(Resource)
class ResourceAdmin(HasImageAdminMixin, PageBaseAdmin):
    date_hierarchy = 'date'

    search_fields = PageBaseAdmin.search_fields + ('content', 'summary',)

    list_display = ['get_image', 'title', 'date', 'page', 'type', 'is_online']
    list_display_links = ['get_image', 'title']
    list_editable = ['is_online']
    list_filter = ['page', 'type', 'is_online']

    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'page', 'date', 'type'],
        }),
        ('Resource', {
            'fields': ['image', 'content', 'file', 'publication', 'external_url'],
        }),
        ('Listing', {
            'fields': ['summary', 'featured'],
        }),
        ('Publication', {
            'fields': ['is_online'],
            'classes': ['collapse'],
        }),
    ]

    fieldsets.extend(PageBaseAdmin.fieldsets)

    fieldsets.remove(PageBaseAdmin.NAVIGATION_FIELDS)
    fieldsets.remove(PageBaseAdmin.TITLE_FIELDS)
    fieldsets.remove(OnlineBaseAdmin.PUBLICATION_FIELDS)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['page'].initial = Resources.objects.first()
        return form

    def last_modified(self, obj):
        versions = Version.objects.get_for_object(obj)
        if versions.count() > 0:
            latest_version = versions[:1][0]
            return '{} by {}'.format(
                latest_version.revision.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                latest_version.revision.user
            )
        return "-"
