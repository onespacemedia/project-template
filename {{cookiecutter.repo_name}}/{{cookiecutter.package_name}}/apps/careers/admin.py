from cms.admin import PageBaseAdmin
from django.contrib import admin
from suit.admin import SortableModelAdmin

from .models import Career, Careers


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


@admin.register(Career)
class CareerAdmin(SortableModelAdmin, PageBaseAdmin):
    prepopulated_fields = {'slug': ['title']}

    list_display = ['__str__', 'location', 'closing_date', 'is_online']
    list_editable = ['is_online']
    list_filter = list(PageBaseAdmin.list_filter) + [CareerOpenClosedListFilter]

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
