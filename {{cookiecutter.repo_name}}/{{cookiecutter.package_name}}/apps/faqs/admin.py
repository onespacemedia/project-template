from adminsortable2.admin import SortableAdminMixin
from cms.admin import PageBaseAdmin
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import escape, mark_safe

from .models import Category, Faq, Faqs


@admin.register(Faq)
class FaqAdmin(SortableAdminMixin, PageBaseAdmin):
    list_display = ['__str__', 'render_category', 'is_online', 'order']
    list_editable = ['is_online', 'order']
    search_fields = ['title', 'page', 'category']

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

    def get_queryself(self, request):
        return super().get_queryset(request).select_related('category')

    def render_category(self, obj):
        if not obj.category:
            return '-'
        url = reverse('admin:faqs_category_change', args=[obj.category.pk])
        return mark_safe(f'<a href="{url}">{escape(str(obj.category))}</a>')
    render_category.short_description = 'Category'
    render_category.admin_order_field = 'category'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }
