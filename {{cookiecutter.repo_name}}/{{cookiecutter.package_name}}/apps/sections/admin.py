from cms.apps.pages.admin import page_admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse_lazy
from jet.admin import CompactInline

from ...utils.admin import LinkFieldsLastAdminMixin
from .models import Content, ContentSection


class ContentSectionInline(LinkFieldsLastAdminMixin, CompactInline):
    model = ContentSection
    extra = 0
    filter_horizontal = ['people']
    fk_name = 'page'

    class Media:
        js = [
            reverse_lazy('admin_sections_js'),
            staticfiles_storage.url('cms/js/sortable/sortables.min.js'),
            staticfiles_storage.url('admin/edit_inline/compact_inline.js'),
        ]

        css = {
            'all': [
                staticfiles_storage.url('css/admin-sections.css'),
                staticfiles_storage.url('admin/edit_inline/compact_inline.css'),
            ],
        }


page_admin.register_content_inline(Content, ContentSectionInline)
