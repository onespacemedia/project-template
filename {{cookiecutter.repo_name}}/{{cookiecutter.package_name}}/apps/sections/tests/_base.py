from cms.apps.pages.models import Page
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from watson import search

from ..models import Content, ContentSection


class BaseSectionTestCase(TestCase):
    def setUp(self):
        with search.update_index():
            self.content_type = ContentType.objects.get_for_model(Content)

            self.content_page = Page.objects.create(
                title='Section test',
                content_type_id=self.content_type.pk,
            )

            self.content = Content.objects.create(
                page=self.content_page,
            )

            self.wysiwyg_section = ContentSection.objects.create(
                type='text-wysiwyg',
                page=self.content_page,
                kicker='Kicker test',
                title='Title test',
                content='<p>Text test</p>',
                link_url='/link-test/',
                link_text='Link test',
                order=2,
            )

            self.hero_section = ContentSection.objects.create(
                type='heroes-hero',
                page=self.content_page,
                kicker='Kicker test',
                title='Title test',
                text='Text test',
                link_url='/link-test/',
                link_text='Link test',
                order=0,
            )
