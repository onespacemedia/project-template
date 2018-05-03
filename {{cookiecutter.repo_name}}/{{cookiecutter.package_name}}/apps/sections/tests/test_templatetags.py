from ..templatetags.sections import render_section
from ._base import BaseSectionTestCase


class SectionTemplateTagsTestCase(BaseSectionTestCase):
    def test_render_section(self):
        # Disable section creation,
        with self.settings(DEBUG=False):
            text = render_section({}, self.wysiwyg_section)

        # Ensure all fields are actually being rendered.
        self.assertIn('Kicker test', text)
        self.assertIn('Title test', text)
        self.assertIn('<p>Text test</p>', text)
        self.assertIn('href="/link-test/"', text)
        self.assertIn('Link test', text)
