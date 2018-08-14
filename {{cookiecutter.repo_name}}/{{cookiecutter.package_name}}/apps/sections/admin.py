from cms.apps.pages.admin import page_admin
from django.core.urlresolvers import reverse_lazy
from jet.admin import CompactInline

from .models import Content, ContentSection


class ContentSectionInline(CompactInline):
    model = ContentSection
    extra = 0
    filter_horizontal = ['people']
    fk_name = 'page'

    class Media(object):
        js = [reverse_lazy('admin_sections_js')]

        css = {
            'all': ['/static/css/admin-sections.css'],
        }


page_admin.register_content_inline(Content, ContentSectionInline)
