from django.test import TestCase

from ..models import SectionBase, get_section_types_flat


class SectionModelsTestCase(TestCase):
    def test_get_section_types_flat(self):
        section_types = get_section_types_flat()
        self.assertIsInstance(section_types, list)
        self.assertIsInstance(section_types[0], dict)

    def test_section_fields(self):
        section_fields = [f.name for f in SectionBase._meta.get_fields()]
        section_types = get_section_types_flat()
        for section_type in section_types:
            for field in section_type['fields']:
                self.assertIn(field, section_type['fields'])
