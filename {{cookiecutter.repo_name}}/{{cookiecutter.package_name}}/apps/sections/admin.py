from cms.apps.pages.admin import page_admin
from django.core.urlresolvers import reverse_lazy
from suit.admin import SortableStackedInline

from .models import Content, ContentSection


class ContentSectionInline(SortableStackedInline):
    model = ContentSection
    extra = 0
    filter_horizontal = ['people']

    class Media(object):
        js = [reverse_lazy('admin_sections_js')]

        css = {
            'all': ['/static/css/admin-sections.css'],
        }


page_admin.register_content_inline(Content, ContentSectionInline)
