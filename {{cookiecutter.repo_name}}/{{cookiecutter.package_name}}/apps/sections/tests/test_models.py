from django.test import TestCase

from ..models import SectionBase, SECTION_TYPES


class SectionModelsTestCase(TestCase):
    def test_get_section_types_flat(self):
        self.assertIsInstance(SECTION_TYPES, list)
        self.assertIsInstance(SECTION_TYPES[0], dict)

    def test_section_fields(self):
        section_fields = [f.name for f in SectionBase._meta.get_fields()]
        for section_type in SECTION_TYPES:
            for field in section_type['fields']:
                self.assertIn(field, section_type['fields'])
