from collections import defaultdict
from importlib.util import module_from_spec, spec_from_file_location
from os import path, walk

from django.conf import settings
from django.utils.text import slugify


def generate_section_types():
    templates_dir = path.join(settings.SITE_ROOT, 'apps', 'sections', 'templates', 'sections', 'types')
    _, dirs, _ = next(walk(templates_dir))

    section_types = []

    for directory in dirs:
        config_file = path.join(templates_dir, directory, 'config.py')
        section_template = path.join(templates_dir, directory, 'template.html')
        section_js = path.join(templates_dir, directory, 'index.js')

        if not path.isfile(config_file):
            raise OSError(f'Configuration file missing for section: {directory}')

        if not path.isfile(section_template):
            raise OSError(f'No template for section: {directory}')

        spec = spec_from_file_location(f'{directory}.config', config_file)
        config = module_from_spec(spec)
        spec.loader.exec_module(config)

        section_data = getattr(config, 'CONFIG')

        if not section_data:
            raise ValueError(f'No configuration information found for section: {directory}')

        if not section_data.get('name'):
            raise OSError(f'No name specified for section: {directory}')

        if not section_data.get('slug'):
            section_data['slug'] = slugify(section_data['name'])

        if not section_data.get('javascript'):
            section_data['javascript'] = path.isfile(section_js)
            section_data['directory_name'] = directory

        section_types.append(section_data)

    return section_types


def get_section_type_choices(types, order=None):
    categories = defaultdict(list)
    for section in types:
        categories[section.get('category', 'other').capitalize()].append(
            (section['slug'], section['name'])
        )

    choices = [(key, value) for key, value in categories.items()]

    if not order:
        return choices

    order = [x.lower() for x in order]

    for choice in choices:
        category = choice[0]
        if not category.lower() in order:
            order.append(category)

    ordered_choices = []
    for value in order:
        for choice in choices:
            if choice[0].lower() == value:
                ordered_choices.append(choice)

    return ordered_choices
