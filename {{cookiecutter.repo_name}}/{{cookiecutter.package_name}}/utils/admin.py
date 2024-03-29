from cms.apps.pages.models import ContentBase
from django.contrib import admin
from django.db.models import Q
from django.urls import NoReverseMatch, reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail

try:
    from ..apps.sections.models import ContentSection, SectionBase
except ImportError:
    class ContentSection:
        pass

    class SectionBase:
        pass


class LinkFieldsLastAdminMixin:
    '''
    A mixin for ModelAdmin & its inlines which ensures that fields from
    HasLinkMixin always come last (which almost invariably makes most sense).
    '''
    def get_fields(self, request, obj=None):
        '''Make fields from HasLinkMixin last.'''
        fields = list(super().get_fields(request, obj=obj))
        for field in ['link_page', 'link_url', 'link_text']:
            fields.remove(field)
            fields.append(field)
        return fields


class UsedOnAdminMixin:
    '''
    Designed for components that are used inside pages.

    Usage:

    @admin.register(YourModel)
    class YourModelAdmin(UsedOnAdminMixin):
        list_display = ['....', 'pages_used_on']

    '''

    def pages_used_on(self, obj):
        pages_used = []

        for rel in obj._meta.related_objects:
            accessor_name = rel.get_accessor_name()

            for rel_obj in getattr(obj, accessor_name).all():
                url = None
                title = None

                if isinstance(rel_obj, ContentBase):
                    url = u'{}#id_{}'.format(
                        reverse('admin:pages_page_change', args=[rel_obj.page_id]),
                        rel.field.name,
                    )

                    title = rel_obj

                elif isinstance(rel_obj, ContentSection):
                    index = list(rel_obj.page.contentsection_set.all()).index(rel_obj)

                    fragment = u'{}-{}'.format(
                        rel.get_accessor_name(),
                        index
                    )

                    url = u'{}#{}'.format(
                        reverse('admin:pages_page_change', args=[rel_obj.page_id]),
                        fragment,
                    )

                    title = rel_obj.page.title

                # Not a page. But it is a BaseSection instance. Let's try and
                # guess its admin URL.
                elif isinstance(rel_obj, SectionBase) and hasattr(rel_obj, 'page'):
                    guess_url = u'admin:{}_{}_change'.format(
                        rel_obj.page._meta.app_label,
                        rel_obj.page._meta.model_name,
                    )

                    try:
                        title = rel_obj.page
                        url = reverse(guess_url, args=[rel_obj.page_id])

                    except NoReverseMatch:
                        continue

                if title and url:
                    pages_used.append(u'<a href="{}">{}</a>'.format(
                        url, escape(title)
                    ))

        return u', '.join(pages_used)

    pages_used_on.short_description = 'Pages used on'
    pages_used_on.allow_tags = True


class HasImageAdminMixin:
    '''
    A helper to add a thumbnail into admin list views, for models that have an
    ImageRefField field.

    Inherit from this and add `get_image` to your `list_display` in the place
    you want to show the image. If you have the image set as the first column
    in the list, you'll probably want to override `list_display_links` as
    well.

    class MyModelAdmin(HasImageAdminMixin, admin.ModelAdmin):
        list_display = ['get_image', '__str__']
        list_display_links = ['get_image', '__str__']

    It assumes that the field is called "image"; if it's called something else
    on your model, override the `image_field` attribute, e.g.:

    class MyModelAdmin(HasImageAdminMixin, admin.ModelAdmin):
        image_field = 'photo'
    '''
    image_field = 'image'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(self.image_field)

    def get_image_reference(self, obj):
        return getattr(obj, self.image_field)

    def get_image(self, obj):
        """Generates a thumbnail of the image."""
        image = self.get_image_reference(obj)
        if not image:
            return ''
        try:
            thumbnail = get_thumbnail(image.file, '100x66', quality=99)
            return mark_safe('<img src="{}" width="{}" height="{}" alt=""/>'.format(
                thumbnail.url,
                thumbnail.width,
                thumbnail.height,
            ))
        except:  # pylint:disable=bare-except
            # ^^ We allow bare exceptions above because of the vast number
            # of exceptions that can occur; it could be IOError for bad
            # permissions, ValueError or ZeroDivisionError with invalid files,
            # etc.
            return '(corrupt image?)'
    get_image.short_description = 'Image'


class SEOQualityControlFilter(admin.SimpleListFilter):
    '''
    A filter for models deriving from SearchMetaBase, to find pages with
    incomplete SEO, OpenGraph or Twitter card information.

    Usage:

    class MyModelAdmin(SearchMetaBaseAdmin):
        list_filter = [SEOQualityControlFilter]
    '''

    title = 'Quality control'

    parameter_name = 'seo_quality_control'

    def lookups(self, request, model_admin):
        return (
            ('no-meta-description', 'No meta description'),
            ('no-browser-title', 'No browser title'),
            ('incomplete-opengraph-fields', 'Incomplete Open Graph fields'),
            ('no-og-image', 'No Open Graph image'),
            ('incomplete-twitter-fields', 'Incomplete Twitter card fields'),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        options = {
            'no-meta-description': lambda qs: qs.filter(Q(meta_description=None) | Q(meta_description='')),
            'no-browser-title': lambda qs: qs.filter(Q(browser_title=None) | Q(browser_title='')),
            'incomplete-opengraph-fields': lambda qs: qs.filter(Q(og_description=None) | Q(og_description='') | Q(og_image=None)),
            'no-og-image': lambda qs: qs.filter(og_image=None),
            'incomplete-twitter-fields': lambda qs: qs.filter(Q(twitter_description=None) | Q(twitter_description='') | Q(og_image=None)),
        }

        return options[self.value()](queryset)
