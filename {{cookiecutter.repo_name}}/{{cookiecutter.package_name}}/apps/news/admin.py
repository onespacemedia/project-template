"""Admin settings for the CMS news app."""
from adminsortable2.admin import SortableAdminMixin
from cms.admin import OnlineBaseAdmin, PageBaseAdmin
from cms.plugins.moderation.models import APPROVED, STATUS_CHOICES
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import escape, mark_safe
from reversion.admin import VersionAdmin
from reversion.models import Version

from ...utils.admin import HasImageAdminMixin, SEOQualityControlFilter
from .models import Article, Category, get_default_news_feed


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, VersionAdmin):
    list_display = ['__str__']
    prepopulated_fields = {'slug': ['title']}


class ArticleAdmin(HasImageAdminMixin, PageBaseAdmin, VersionAdmin):
    date_hierarchy = 'date'

    search_fields = PageBaseAdmin.search_fields + ('content', 'summary',)

    list_display = ['get_image', 'title', 'date', 'render_categories', 'featured', 'is_online', 'last_modified']
    list_display_links = ['get_image', 'title']
    list_editable = ['featured', 'is_online']
    list_filter = ['page', 'categories', 'featured', 'is_online', SEOQualityControlFilter]

    if getattr(settings, 'NEWS_APPROVAL_SYSTEM', False):
        list_filter.append('status')

    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'page', 'content', 'date', 'status'],
        }),
        ('Content', {
            'fields': ['featured', 'summary', 'image', 'card_image', 'categories'{% if cookiecutter.people == 'yes' %}, 'author'{% endif %}],
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

    filter_horizontal = ['categories']

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ArticleAdmin, self).get_fieldsets(request, obj)

        if not getattr(settings, 'NEWS_APPROVAL_SYSTEM', False):
            for fieldset in fieldsets:
                fieldset[1]['fields'] = tuple(x for x in fieldset[1]['fields'] if x != 'status')

        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['page'].initial = get_default_news_feed()
        return form

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('categories')

    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        """
        Give people who have the permission to approve articles an extra
        option to change the status of an Article to approved
        """
        if request:
            choices_list = STATUS_CHOICES
            if getattr(settings, 'NEWS_APPROVAL_SYSTEM', False) and not request.user.has_perm('news.can_approve_articles'):
                choices_list = [x for x in STATUS_CHOICES if x[0] != APPROVED]

            if db_field.name == 'status':
                kwargs['choices'] = choices_list

        return super(ArticleAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

    def get_image_reference(self, obj):
        return obj.card_image or obj.image

    def render_categories(self, obj):
        categories = obj.categories.all()
        if not categories:
            return '(None)'
        parts = []

        for category in categories:
            url = reverse('admin:news_category_change', args=[category.pk])
            parts.append(f'<a href="{url}">{escape(category)}</a>')

        return mark_safe(', '.join(parts))

    def last_modified(self, obj):
        versions = Version.objects.get_for_object(obj)
        if versions.count() > 0:
            latest_version = versions[:1][0]
            return '{} by {}'.format(
                latest_version.revision.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                latest_version.revision.user
            )
        return "-"

    render_categories.short_description = 'Categories'


admin.site.register(Article, ArticleAdmin)
