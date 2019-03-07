from cms.admin import PageBaseAdmin
from django.contrib import admin
from reversion.models import Version
from suit.admin import SortableModelAdmin

from ...utils.admin import HasImageAdminMixin
from .models import Category, Event, Events


@admin.register(Category)
class CategoryAdmin(SortableModelAdmin):
    list_display = ['__str__']
    prepopulated_fields = {'slug': ['title']}


@admin.register(Event)
class EventAdmin(HasImageAdminMixin, PageBaseAdmin):
    list_display = ['get_image', '__str__', 'start_date', 'end_date', 'featured', 'is_online', 'last_modified']
    list_display_links = ['get_image', '__str__']
    list_editable = ['featured', 'is_online']
    list_filter = ['page', 'categories', 'featured', 'is_online']

    filter_horizontal = ['categories']

    fieldsets = [
        (None, {
            'fields': ['page', 'title', 'slug', 'featured'],
        }),
        ('Date', {
            'fields': [('start_date', 'end_date')]
        }),
        ('Content', {
            'fields': ['image', 'summary', 'content'],
        }),
        PageBaseAdmin.PUBLICATION_FIELDS,
        PageBaseAdmin.SEO_FIELDS,
        PageBaseAdmin.OPENGRAPH_FIELDS,
        PageBaseAdmin.OPENGRAPH_TWITTER_FIELDS
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventAdmin, self).get_form(request, obj, **kwargs)

        try:
            form.base_fields['page'].initial = Events.objects.first()
        except IndexError:
            pass

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
