from __future__ import print_function

from cms.apps.media.models import ImageRefField
from cms.models import HtmlField
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import render_to_response
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from ...utils.models import HasLinkMixin, ProjectContentBase, VideoMixin
{% if cookiecutter.news == 'yes' %}from ..news.models import Article{% endif %}

SECTION_TYPES = (
    ('Heroes', {
        'sections': [
            ('landing-hero', {
                'fields': ['kicker', 'title', 'text', 'image', 'link_text', 'link_page', 'link_url'],
                'search': ['kicker', 'title', 'text'],
                'required': ['title', 'image'],
                'help_text': {
                    'kicker': 'If this is left blank it will inherit the title of the page.',
                },
            }),
        ],
    }),
    ('Images', {
        'sections': [
            ('full-width', {
                'fields': ['image', 'mobile_image'],
                'required': ['image']
            }),
            ('split', {
                'fields': ['kicker', 'title', 'content', 'image', 'image_side', 'link_text', 'link_page', 'link_url'],
                'search': ['kicker', 'title', 'content'],
                'required': ['title', 'image'],
            }),
        ]
    }),
    ('Text', {
        'sections': [
            ('wysiwyg', {
                'name': 'Rich text',
                'fields': ['background_colour', 'kicker', 'title', 'content', 'link_text', 'link_page', 'link_url'],
                'search': ['kicker', 'title', 'content'],
            }),
            ('dual-column', {
                'fields': ['background_colour', 'kicker', 'title', 'left_column', 'right_column', 'link_text', 'link_page', 'link_url'],
                'search': ['kicker', 'title', 'left_column', 'right_column'],
            }),
        ],
    }),
    ('Components', {
        'sections': [{% if cookiecutter.news == 'yes' %}
            ('latest-news', {
                'fields': ['background_colour', 'title', 'news_feed', 'link_text', 'link_page', 'link_url'],
                'search': ['title'],
                'required': ['news_feed'],
            }),{% endif %}
            ('statistics', {
                'fields': ['background_colour', 'stat_set'],
                'required': ['stat_set'],
            }),
        ],
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


class SectionBase(HasLinkMixin, VideoMixin):

    type = models.CharField(
        choices=get_section_type_choices(SECTION_TYPES),
        max_length=100,
    )

    background_colour = models.CharField(
        max_length=255,
        choices=[
            ('transparent', 'Transparent'),
        ],
        default='transparent',
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

    left_column = HtmlField(
        blank=True,
        null=True,
    )

    right_column = HtmlField(
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

    stat_set = models.ForeignKey(
        'components.StatSet',
        blank=True,
        null=True,
    )
{% if cookiecutter.news == 'yes' %}
    news_feed = models.ForeignKey(
        'news.NewsFeed',
        blank=True,
        null=True,
    ){% endif %}

    order = models.PositiveIntegerField(
        default=0,
        help_text='Order which the section will be displayed',
    )

    class Meta:
        abstract = True
        ordering = ['order']

    def __str__(self):
        return self.get_type_display()

    def clean(self):
        required = [getattr(self, field) for field in self.definition.get('required', [])]

        if not all(required):
            fields_str = ''
            fields_len = len(required)
            fields = {}

            for index, field in enumerate(self.definition.get('required', [])):
                fields[field] = ValidationError(f'This field is required for this section type', code='required')
                connector = ', '

                if index == fields_len - 2:
                    connector = ' and '
                elif index == fields_len - 1:
                    connector = ''

                anchor = f'id_{self._meta.model_name}_set-{self.order}-{field}'
                fields_str += f'<a href="#{anchor}">{field.title()}</a>{connector}'

            fields['__all__'] = ValidationError(mark_safe(f'{fields_str} fields are required'), code='error')

            raise ValidationError(fields)

        if self.link_text and (not self.link_page and not self.link_url):
            raise ValidationError({
                'link_page': 'Please provide either a "Link Page" or a "Link URL"',
            })

        super().clean()

    @cached_property
    def cache_key(self):
        return f'{self._meta.app_label}.{self._meta.model_name}.{self.pk}'

    @cached_property
    def definition(self):
        '''
        Returns the definition in SECTION_TYPES for this section instance.
        '''
        for section_group in SECTION_TYPES:
            for section_type in section_group[1]['sections']:
                section_label = slugify('{}-{}'.format(section_group[0], section_type[0]))

                if section_label == self.type:
                    return section_type[1]

        return {
            'fields': [],
            'required': [],
        }

    @property
    def template(self):
        folder_name = self.type.split('-')[0]
        file_name = '-'.join(self.type.split('-')[1:])

        return {
            'folder': folder_name,
            'file_name': f'{file_name}.html'
        }

    def get_searchable_text(self):
        '''
        Returns a blob of text suitable for searching. It will search all
        fields in its definition's 'search'. If that field is a ForeignKey,
        and the referenced object implements a get_searchable_text method,
        it will include the result of calling that method too.
        '''

        search_fields = self.definition.get('search', [])

        search_text_items = []

        for field in search_fields:
            search_item = getattr(self, field)

            if isinstance(search_item, models.Model):
                if hasattr(search_item, 'get_searchable_text'):
                    search_text_items.append(search_item.get_searchable_text())

            elif search_item:
                search_text_items.append(strip_tags(str(search_item)))

        return ' '.join(search_text_items)
{% if cookiecutter.news == 'yes' %}
    def get_latest_news(self):
        return Article.objects.filter(
            page__page=self.news_feed
        ).prefetch_related(
            'categories',
        ).select_related(
            'image',
            'card_image',
        ).order_by(
            '-date'
        )[:3]{% endif %}


class ContentSection(SectionBase):

    page = models.ForeignKey(
        'pages.Page',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.get_type_display()


class SectionedContentBase(ProjectContentBase):
    '''
    A helper ContentBase derivative that ensures that the page's sectioned
    content is indexed by Watson.
    '''

    sections_attribute = 'contentsection_set'

    class Meta:
        abstract = True

    def get_searchable_text(self):
        text = super().get_searchable_text()
        sections = getattr(self.page, self.sections_attribute).all()

        for section in sections:
            text = text + ' ' + section.get_searchable_text()

        return text


class Content(SectionedContentBase):

    icon = 'cms-icons/sections.png'

    def __str__(self):
        return self.page.title
