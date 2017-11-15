from __future__ import print_function

from cms.apps.media.models import ImageRefField
from cms.apps.pages.models import ContentBase, Page
from cms.models import HtmlField
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import render_to_response
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import slugify

SECTION_TYPES = (
    ('Heroes', {
        'sections': [
            ('landing-hero', {
                'fields': ['kicker', 'title', 'text', 'image', 'link_text', 'link_page', 'link_url'],
                'search': ['kicker', 'title', 'text'],
                'required': ['title', 'image'],
                'help_text': {
                    'kicker': 'If this is left blank it will inherit the pages title',
                },
            }),
        ]
    }),
    ('Images', {
        'sections': [
            ('full-width', {
                'fields': ['image', 'mobile_image'],
                'required': ['image']
            }),
            ('split', {
                'fields': ['kicker', 'title', 'text', 'image', 'image_side' 'link_text', 'link_page', 'link_url'],
                'search': ['kicker', 'title', 'text'],
                'required': ['title', 'image'],
            }),
        ]
    }),
    ('Text', {
        'sections': [
            ('centered', {
                'fields': ['background_colour', 'kicker', 'title', 'text', 'link_text', 'link_page', 'link_url'],
                'search': ['kicker', 'title', 'text'],
                'required': ['title'],
            }),
            ('dual-column', {
                'fields': ['kicker', 'title', 'text', 'link_text', 'link_page', 'link_url'],
                'search': ['kicker', 'title', 'text'],
                'required': ['title'],
            }),
        ]
    }),
)


def get_section_name(obj):
    if 'name' in obj[1]:
        return obj[1]['name']

    return obj[0][0].upper() + obj[0][1:].replace('-', ' ')


def get_section_types_flat():
    '''Gets a list of section types as a flat list of dictionaries.'''
    types = []
    # Loop section groups.
    for group in SECTION_TYPES:
        # Every section that appears in the optgroup
        for section_type in group[1]['sections']:
            types.append({
                'slug': f'{slugify(group[0])}-{section_type[0]}',
                'name': f'{group[0]} - {get_section_name(section_type)}',
                'fields': section_type[1].get('fields', []),
                'search': section_type[1].get('search', []),
                'required': section_type[1].get('required', []),
                'help_text': section_type[1].get('help_text', {}),
            })
    return types


def sections_js(request):
    model_fields = [f.name for f in SectionBase._meta.get_fields()]
    # Since our sections aren't at the top level we'll need to create an array
    # of them when we are iterating
    sections = get_section_types_flat()

    for section_type in sections:
        for field in section_type['fields']:
            if field not in model_fields:
                print(f"NOTE: Field `{field}` is referenced by section type `{section_type['name']}`, but doesn't exist.")

    return render_to_response('admin/pages/page/sections.js', {
        'types': sections,
    }, content_type='application/javascript')


def get_section_type_choices(types):
    # Will be used to build up our optgroups
    groups = []

    for section_group in SECTION_TYPES:
        label = section_group[0]
        content = section_group[1]

        # We'll need to build a tuple of the section option value & option name
        sections = []

        for section in content['sections']:
            section_label = slugify(f'{section_group[0]}-{section[0]}')

            sections.append(
                (slugify(section_label), get_section_name(section)))

        groups.append((label, sections))

    return groups


class SectionBase(models.Model):

    page = models.ForeignKey(
        Page,
    )

    type = models.CharField(
        choices=get_section_type_choices(SECTION_TYPES),
        max_length=100,
    )

    background_colour = models.CharField(
        max_length=255,
        choices=[
            ('white', 'White'),
        ],
        default='white',
    )

    kicker = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    title = models.CharField(
        max_length=140,
        blank=True,
        null=True,
    )

    text = models.TextField(
        blank=True,
        null=True,
    )

    content = HtmlField(
        blank=True,
        null=True,
    )

    image = ImageRefField(
        blank=True,
        null=True,
    )

    mobile_image = ImageRefField(
        blank=True,
        null=True,
    )

    image_side = models.CharField(
        max_length=10,
        choices=[
            ('left', 'Left'),
            ('right', 'Right'),
        ],
        default='left',
    )

    link_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    link_page = models.ForeignKey(
        'pages.Page',
        blank=True,
        null=True,
        help_text='Use this to link to an internal page.',
        related_name='+'
    )

    link_url = models.CharField(
        'link URL',
        max_length=200,
        blank=True,
        null=True,
        help_text='Use this to link to any other URL.',
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text='Order which the section will be displayed',
    )

    class Meta:
        abstract = True
        ordering = ['order']

    def __str__(self):
        return next((x for x in get_section_types_flat() if x['slug'] == self.type), None)['name']

    def clean(self):
        sections = get_section_types_flat()

        for section in sections:
            if self.type == section['slug']:
                required = [getattr(self, field)
                            for field in section['required']]
                if not all(required):
                    fields_str = ''
                    fields_len = len(section['required'])
                    fields = {}

                    for index, field in enumerate(section['required']):
                        fields[field] = ValidationError(f'Please provide an {field}', code='required')
                        connector = ', '

                        if index == fields_len - 2:
                            connector = ' and '
                        elif index == fields_len - 1:
                            connector = ''

                        anchor = f'id_{self._meta.model_name}_set-{self.order}-{field}'
                        fields_str += f'<a href="#{anchor}">{field.title()}</a>{connector}'

                    fields['__all__'] = ValidationError(mark_safe(f"{fields_str} fields are required"), code='error')

                    raise ValidationError(fields)

        if self.link_text and (not self.link_page or not self.link_url):
            raise ValidationError({
                'link_page': 'Please supply 1 of "link page" or "link URL"',
            })

    @property
    def template(self):
        folder_name = self.type.split('-')[0]
        file_name = '-'.join(self.type.split('-')[1:])

        return {
            'folder': folder_name,
            'file_name': f'{file_name}.html'
        }

    @property
    def has_link(self):
        return self.link_location and self.link_text

    @cached_property
    def link_location(self):
        if self.link_page_id:
            try:
                return self.link_page.get_absolute_url()
            except Page.DoesNotExist:
                pass
        return self.link_url

    def get_searchable_text(self):
        """Returns a blob of text suitable for searching."""

        # Let's look for the options for our section type.
        for section_group in SECTION_TYPES:
            for section_type in section_group[1]['sections']:
                section_label = slugify(
                    '{}-{}'.format(section_group[0], section_type[0]))

                if not section_label == self.type:
                    continue

                # If we defeated the above clause then we have the options
                # for the right section type.
                section_options = section_type[1]

                # Don't require that search_fields is set.
                if 'search_fields' not in section_options:
                    continue

                search_fields = section_options['search_fields']

                search_text_items = []
                for field in search_fields:
                    search_item = getattr(self, field)
                    if search_item:
                        search_text_items.append(strip_tags(search_item))

                return u'\n'.join(search_text_items)

        return ''


class ContentSection(SectionBase):
    pass


class Content(ContentBase):

    icon = 'cms-icons/sections.png'
