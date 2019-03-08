from ._base import ResourcesBaseTestCase


class ResourcesModelsTestCase(ResourcesBaseTestCase):
    def test_get_absolute_url(self):
        self.assertEqual(self.whitepaper.get_absolute_url(), self.file.get_absolute_url())
        self.assertEqual(self.case_study.get_absolute_url(), '/case-study-test/')
        self.assertEqual(self.video.get_absolute_url(), 'https://www.example.com')

    def test_file_extension(self):
        self.assertEqual(self.whitepaper.file_extension, 'pdf')

    def test_get_related(self):
        self.assertNotEqual(len(self.whitepaper.get_related_resources()), 0)

    def test_get_summary(self):
        self.assertEqual(self.case_study.get_summary(), 'Article content goes here & <>')
