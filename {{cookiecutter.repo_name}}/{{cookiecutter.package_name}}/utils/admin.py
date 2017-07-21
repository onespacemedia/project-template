from cms.apps.pages.models import ContentBase
from django.core.urlresolvers import NoReverseMatch, reverse
from django.utils.html import escape

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
