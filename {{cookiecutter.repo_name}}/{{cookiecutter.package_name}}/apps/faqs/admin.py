from cms.admin import PageBaseAdmin
from django.contrib import admin
from suit.admin import SortableModelAdmin

from .models import Category, Faq, Faqs


@admin.register(Faq)
class FaqAdmin(SortableModelAdmin, PageBaseAdmin):
    list_display = ['__str__', 'category', 'is_online', 'order']
    list_editable = ['is_online', 'order']

    fieldsets = [
        (None, {
            'fields': ['page', 'category', 'title', 'slug'],
        }),
        ('Content', {
            'fields': ['question', 'answer'],
        }),
        PageBaseAdmin.PUBLICATION_FIELDS,
        PageBaseAdmin.NAVIGATION_FIELDS,
        PageBaseAdmin.SEO_FIELDS,
        PageBaseAdmin.OPENGRAPH_FIELDS,
        PageBaseAdmin.OPENGRAPH_TWITTER_FIELDS,
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(FaqAdmin, self).get_form(request, obj, **kwargs)

        try:
            form.base_fields['page'].initial = Faqs.objects.first()
        except IndexError:
            pass

        return form


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }
