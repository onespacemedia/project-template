from adminsortable2.admin import SortableAdminMixin
from cms.admin import PageBaseAdmin
from django.contrib import admin
from reversion.admin import VersionAdmin

from ...utils.admin import SEOQualityControlFilter
from .models import Career, CareerLocation, Careers


class CareerOpenClosedListFilter(admin.SimpleListFilter):
    title = 'Status'

    parameter_name = 'application_status'

    def lookups(self, request, model_admin):
        return (
            ('open', 'Open'),
            ('closed', 'Closed')
        )

    def queryset(self, request, queryset):
        if self.value() == 'closed':
            return queryset.select_closed()

        if self.value() == 'open':
            return queryset.select_open()

        return queryset


@admin.register(Career)
class CareerAdmin(SortableAdminMixin, PageBaseAdmin):
    prepopulated_fields = {'slug': ['title']}

    list_display = ['__str__', 'location', 'closing_date', 'is_online']
    list_editable = ['is_online']
    list_filter = list(PageBaseAdmin.list_filter) + [CareerOpenClosedListFilter, SEOQualityControlFilter]

    fieldsets = [
        (None, {
            'fields': ['page', 'title', 'slug', 'closing_date'],
        }),
        ('Content', {
            'fields': ['location', 'summary', 'description'],
        }),
        ('Applying', {
            'fields': ['email_address', 'application_url'],
        }),
        ('Schema fields', {
            'fields': ['employment_type', 'education_requirements', 'experience_requirements', 'qualifications',
                       'responsibilities', 'skills', 'work_hours', 'estimated_salary', 'base_salary']
        }),
        PageBaseAdmin.PUBLICATION_FIELDS,
        PageBaseAdmin.SEO_FIELDS,
        PageBaseAdmin.OPENGRAPH_FIELDS,
        PageBaseAdmin.OPENGRAPH_TWITTER_FIELDS,
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(CareerAdmin, self).get_form(request, obj, **kwargs)

        try:
            form.base_fields['page'].initial = Careers.objects.first()
        except IndexError:
            pass

        return form


@admin.register(CareerLocation)
class LocationAdmin(VersionAdmin):

    fieldsets = (
        (None, {
            'fields': ['title']
        }),
        ('Address', {
            'fields': ['street_address', 'city', 'region', 'postcode', 'country']
        }),
    )
