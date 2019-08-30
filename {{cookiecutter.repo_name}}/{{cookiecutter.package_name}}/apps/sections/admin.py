from cms.apps.pages.admin import page_admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse_lazy
from osm_jet.admin import JetCompactInline

from ...utils.admin import LinkFieldsLastAdminMixin
from .models import Content, ContentSection


class ContentSectionInline(LinkFieldsLastAdminMixin, JetCompactInline):
    model = ContentSection
    extra = 0
    filter_horizontal = ['people']
    fk_name = 'page'

    class Media:
        js = [
            reverse_lazy('admin_sections_js')
        ] + JetCompactInline.Media.js

        css = {
            'all': [
                staticfiles_storage.url('css/admin-sections.css'),
            ] + JetCompactInline.Media.css['all']
        }


page_admin.register_content_inline(Content, ContentSectionInline)
