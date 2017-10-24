from django.test import TestCase

from ..templatetags.site import md


class TemplateTagsTestCase(TestCase):
    def test_md(self):
        # Test with the default inline=True
        tests = [
            (None, ''),
            # Make sure it's not wrapped in <p>.
            ('onespacemedia', 'onespacemedia'),
            # Test bold and italics.
            ('*onespacemedia*', '<em>onespacemedia</em>'),
            ('**onespacemedia**', '<strong>onespacemedia</strong>'),
            ('**one\nspace\nmedia**', '<strong>one<br>space<br>media</strong>'),
        ]

        for test in tests:
            self.assertEquals(md(test[0]), test[1])

        # Test it without the 'inline' option.
        tests = [
            (None, ''),
            # Make sure it's wrapped in <p>
            ('onespacemedia', '<p>onespacemedia</p>'),
            # Test bold and italics.
            ('*onespacemedia*', '<p><em>onespacemedia</em></p>'),
            ('**onespacemedia**', '<p><strong>onespacemedia</strong></p>'),
            ('onespace\n\nmedia', '<p>onespace</p>\n<p>media</p>'),
        ]

        for test in tests:
            self.assertEquals(md(test[0], inline=False), test[1])
