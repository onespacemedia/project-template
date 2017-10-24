from cms.apps.pages.models import ContentBase
from django.core.urlresolvers import NoReverseMatch, reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail

try:
    from ..apps.sections.models import ContentSection, SectionBase
except ImportError:
    class ContentSection(object):
        pass

    class SectionBase(object):
        pass


class UsedOnAdminMixin(object):
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


class HasImageAdminMixin(object):
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

    def get_image(self, obj):
        """Generates a thumbnail of the image."""
        image = getattr(obj, self.image_field)
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
