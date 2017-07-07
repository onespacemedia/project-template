from cms.admin import PageBaseAdmin
from django.contrib import admin
from suit.admin import SortableModelAdmin

from .models import Career, Careers


@admin.register(Career)
class CareerAdmin(SortableModelAdmin, PageBaseAdmin):
    prepopulated_fields = {'slug': ['title']}

    list_display = ['__str__', 'is_online', 'order']
    list_editable = ['is_online', 'order']

    fieldsets = [
        (None, {
            'fields': ['page', 'title', 'slug'],
        }),
        ('Content', {
            'fields': ['location', 'summary', 'description', 'email_address'],
        }),
        PageBaseAdmin.PUBLICATION_FIELDS,
        PageBaseAdmin.NAVIGATION_FIELDS,
        PageBaseAdmin.SEO_FIELDS,
        PageBaseAdmin.OPENGRAPH_FIELDS,
        PageBaseAdmin.OPENGRAPH_TWITTER_FIELDS
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(CareerAdmin, self).get_form(request, obj, **kwargs)

        try:
            form.base_fields['page'].initial = Careers.objects.first()
        except IndexError:
            pass

        return form
