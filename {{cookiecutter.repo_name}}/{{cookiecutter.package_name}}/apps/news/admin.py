"""Admin settings for the CMS news app."""

from cms.admin import OnlineBaseAdmin, PageBaseAdmin
from django.conf import settings
from django.contrib import admin
from reversion.admin import VersionAdmin
from reversion.models import Version

from ...utils.admin import HasImageAdminMixin
from .models import STATUS_CHOICES, Article, Category, get_default_news_feed


@admin.register(Category)
class CategoryAdmin(PageBaseAdmin):
    fieldsets = (
        PageBaseAdmin.TITLE_FIELDS,
        PageBaseAdmin.PUBLICATION_FIELDS,
        PageBaseAdmin.NAVIGATION_FIELDS,
        PageBaseAdmin.SEO_FIELDS,
    )
    list_display = ['__str__']


class ArticleAdmin(HasImageAdminMixin, PageBaseAdmin, VersionAdmin):
    date_hierarchy = 'date'

    search_fields = PageBaseAdmin.search_fields + ('content', 'summary',)

    list_display = ['get_image', 'title', 'date', 'render_categories', 'is_online', 'last_modified']
    list_display_links = ['get_image', 'title']
    list_filter = ['is_online', 'categories', 'status']

    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'news_feed', 'date', 'status']
        }),
        ('Content', {
            'fields': ['image', 'content', 'summary', 'categories']
        }),
        ('Publication', {
            'fields': ['is_online'],
            'classes': ['collapse']
        }),
    ]

    fieldsets.extend(PageBaseAdmin.fieldsets)

    fieldsets.remove(PageBaseAdmin.TITLE_FIELDS)
    fieldsets.remove(OnlineBaseAdmin.PUBLICATION_FIELDS)

    raw_id_fields = ['image']

    filter_horizontal = ['categories']

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ArticleAdmin, self).get_fieldsets(request, obj)

        if not getattr(settings, 'NEWS_APPROVAL_SYSTEM', False):
            for fieldset in fieldsets:
                fieldset[1]['fields'] = tuple(x for x in fieldset[1]['fields'] if x != 'status')

        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['news_feed'].initial = get_default_news_feed()
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
                choices_list = [x for x in STATUS_CHOICES if x[0] != 'approved']

            if db_field.name == 'status':
                kwargs['choices'] = choices_list

        return super(ArticleAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

    def render_categories(self, obj):
        categories = obj.categories.all()
        if not categories:
            return '(None)'
        return ', '.join([str(category) for category in categories])

    def last_modified(self, obj):
        versions = Version.objects.get_for_object(obj)
        if versions.count() > 0:
            latest_version = versions[:1][0]
            return "{} by {}".format(
                latest_version.revision.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                latest_version.revision.user
            )
        return "-"

    render_categories.short_description = 'Categories'

admin.site.register(Article, ArticleAdmin)
