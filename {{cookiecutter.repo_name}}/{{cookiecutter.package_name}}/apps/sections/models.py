from __future__ import print_function

from cms.apps.media.models import ImageRefField, VideoRefField
from cms.models import HtmlField
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import render
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from ...utils.models import (HasLinkMixin, HasSecondaryLinkMixin,
                             ProjectContentBase)
from ..news.models import Article
from .utils import generate_section_types, get_section_type_choices

SECTION_ORDER = ['heroes', 'media', 'text', 'components']
SECTION_TYPES = generate_section_types()
PADDING_DEFAULT = 'normal'
PADDING_CHOICES = [
    ('none', 'None'),
    ('small', 'Small'),
    (PADDING_DEFAULT, 'Normal'),
    ('large', 'Large'),
    ('extraLarge', 'Extra large'),
]


def sections_js(request):
    model_fields = [f.name for f in SectionBase._meta.get_fields()]

    for section_type in SECTION_TYPES:
        for field in section_type['fields']:
            if field not in model_fields:
                print(f"NOTE: Field `{field}` is referenced by section type `{section_type['name']}`, but doesn't exist.")

    return render(request, 'admin/pages/page/sections.js', context={
        'types': SECTION_TYPES,
    }, content_type='application/javascript')


class SectionBase(HasSecondaryLinkMixin, HasLinkMixin):
    type = models.CharField(
        choices=get_section_type_choices(SECTION_TYPES, order=SECTION_ORDER),
        max_length=100,
    )

    background_colour = models.CharField(
        max_length=255,
        choices=[
            ('white', 'White'),
            ('black', 'Black'),
        ],
        default='white',
    )

    top_padding = models.CharField(
        max_length=255,
        choices=PADDING_CHOICES,
        default=PADDING_DEFAULT,
    )

    bottom_padding = models.CharField(
        max_length=255,
        choices=PADDING_CHOICES,
        default=PADDING_DEFAULT,
    )

    icon = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text=mark_safe("The name of the icon from <a href='https://fonts.google.com/icons'>Google's material icons</a>. All lowercase and underscores instead of spaces. For example, 'Open in new' becomes 'open_in_new'.")
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

    media_side = models.CharField(
        max_length=10,
        choices=[
            ('left', 'Left'),
            ('right', 'Right'),
        ],
        default='left',
    )

    image = ImageRefField(
        blank=True,
        null=True,
    )

    background_image = ImageRefField(
        blank=True,
        null=True,
    )

    video = VideoRefField(
        blank=True,
        null=True,
    )

    stat_set = models.ForeignKey(
        'components.StatSet',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
{% if cookiecutter.news == 'yes' %}
    news_feed = models.ForeignKey(
        'news.NewsFeed',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    ){% endif %}

    card_set = models.ForeignKey(
        'components.CardSet',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    cards_per_row = models.CharField(
        choices=[
            ('three', 'Three'),
            ('four', 'Four'),
        ],
        max_length=10,
        default='four',
    )

    call_to_action = models.ForeignKey(
        'components.CallToAction',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text='Order which the section will be displayed',
    )

    class Meta:
        abstract = True
        ordering = ['order']

    def __str__(self):
        return next((x for x in SECTION_TYPES if x['slug'] == self.type), None)['name']

    def clean(self):
        sections = SECTION_TYPES

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

    @property
    def template_path(self):
        return f'sections/types/{self.type}/template.html'

    @property
    def cacheable(self):
        # Used to add cases when a section shouldn't be cached
        return True

    def get_searchable_text(self):
        """Returns a blob of text suitable for searching."""

        # Let's look for the options for our section type.
        for section_group in SECTION_TYPES:
            for section_type in section_group[1]['sections']:
                section_label = slugify(f'{section_group[0]}-{section_type[0]}')

                if not section_label == self.type:
                    continue

                # If we defeated the above clause then we have the options
                # for the right section type.
                section_options = section_type[1]

                # Don't require that search_fields is set.
                if 'search' not in section_options:
                    continue

                search_fields = section_options['search']

                search_text_items = []
                for field in search_fields:
                    search_item = getattr(self, field)
                    if search_item:
                        search_text_items.append(strip_tags(search_item))

                return '\n'.join(search_text_items)

        return ''

{% if cookiecutter.news == 'yes' %}
    def get_latest_news(self, count=3):
        return Article.objects.filter(
            page__page=self.news_feed
        ).prefetch_related(
            'categories',
        ).select_related(
            'image',
            'card_image',
        ).order_by(
            '-date'
        )[:count]{% endif %}


class ContentSection(SectionBase):

    page = models.ForeignKey(
        'pages.Page',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return next((x for x in SECTION_TYPES if x['slug'] == self.type), None)['name']


class Content(ProjectContentBase):

    icon = 'cms-icons/sections.png'

    def __str__(self):
        return self.page.title
