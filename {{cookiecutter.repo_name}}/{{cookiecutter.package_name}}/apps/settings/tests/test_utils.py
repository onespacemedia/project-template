from django.test import TestCase

from ..models import Setting
from ..utils import get_setting, get_setting_value


class SettingsUtilsTest(TestCase):
    def setUp(self):
        self.setting = Setting.objects.create(
            name='Test setting',
            key='test-setting',
            type='string',
            string='Value'
        )

    def test_get_setting(self):
        # Test an extant setting
        self.assertEqual(get_setting('test-setting'), self.setting)

        # Test one that doesn't exist.
        self.assertEqual(get_setting('nonexistent-setting'), None)

        # Make sure the value being returned is what we expect.
        self.assertEqual(get_setting_value('test-setting'), 'Value')
        self.assertEqual(get_setting_value('test-setting'), self.setting.value)

        # Make sure default returns work on get_setting_value
        self.assertEqual(get_setting_value('nonexistent-setting'), None)
        self.assertEqual(get_setting_value('nonexistent-setting', 'Setting'), 'Setting')
