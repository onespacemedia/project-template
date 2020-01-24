from cms.apps.media.models import File
from django.test import TestCase
from django.utils.safestring import SafeString

from ..models import Setting


class SettingsModelsTestCase(TestCase):
    def test_setting_str(self):
        setting = Setting(
            name='Test',
        )

        self.assertEqual(str(setting), 'Test')

    def test_setting_value(self):
        setting = Setting(
            type='string',
            string='Testing',
        )
        self.assertEqual(setting.value, 'Testing')

        setting = Setting(
            type='text',
            text='Line\nbreak',
        )
        self.assertEqual(setting.value, 'Line<br>break')
        # Ensure it's marked as safe
        self.assertIsInstance(setting.value, SafeString)

        setting = Setting(
            type='number',
            number=1,
        )
        self.assertEqual(setting.value, 1)

        setting = Setting(
            type='html',
            html='<p>Hi!</p>',
        )
        self.assertEqual(setting.value, '<p>Hi!</p>')
        self.assertIsInstance(setting.value, SafeString)

        fake_file = File(
            title='hi',
        )
        fake_file.id = 1

        setting = Setting(
            type='image',
            image=fake_file,
        )
        self.assertEqual(setting.value, fake_file)
        self.assertIsInstance(setting.value, File)
