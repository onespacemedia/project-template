from cms.apps.pages.models import Page
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from watson import search

from ..models import Resource, Resources, ResourceType


class ResourcesBaseTestCase(TestCase):

    def setUp(self):
        with search.update_index():
            content_type = ContentType.objects.get_for_model(Resources)
            self.page = Page.objects.create(
                content_type=content_type,
                title='Test resources',
                slug='test-resources',
            )

            self.resources_page = Resources.objects.create(
                page=self.page,
                per_page=6,
            )

            self.whitepaper_type = ResourceType(
                title='Whitepaper',
                slug='whitepaper',
            )

            self.case_study_type = ResourceType(
                title='Case study',
                slug='case-study',
            )

            self.video_type = ResourceType(
                title='Video',
                slug='video',
                icon_override='video',
            )

            self.file = SimpleUploadedFile("test.pdf", b"\x00\x01\x02\x03")

            self.whitepaper = Resource(
                page=self.resources_page,
                title='Whitepaper test',
                slug='whitepaper-test',
                file=self.file,
                type=self.whitepaper_type,
            )

            self.case_study = Resource(
                page=self.resources_page,
                title='Case study test',
                slug='case-study-test',
                content='<p>Article content goes here &amp; &lt;&gt;</p>',
                type=self.case_study_type
            )

            self.video = Resource(
                page=self.resources_page,
                title='Video test',
                slug='video-test',
                external_url='https://www.example.com',
                type=self.video_type,
            )
