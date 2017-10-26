from django.test import TestCase

from ..models import Setting
from ..templatetags.settings import get_setting, setting


class SettingsTagsTest(TestCase):
    def setUp(self):
        self.setting = Setting.objects.create(
            name='Test setting',
            key='test-setting',
            type='string',
            string='Value'
        )

    def test_setting(self):
        self.assertEquals(setting('test-setting'), self.setting.value)
        self.assertEquals(setting('test-setting'), 'Value')
        # Test ones that don't exist, and defaults.
        self.assertEquals(setting('no'), None)
        self.assertEquals(setting('no', 'yes'), 'yes')

    def test_get_setting(self):
        # Test one that is real.
        self.assertEquals(get_setting('test-setting'), self.setting)
        self.assertEquals(get_setting('nope'), None)
