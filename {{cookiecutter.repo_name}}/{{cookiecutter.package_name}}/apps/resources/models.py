from html import unescape
from os.path import splitext

from cms.apps.media.models import FileRefField, ImageRefField
from cms.apps.pages.models import ContentBase
from cms.models import HtmlField, PageBase
from cms.templatetags.html import truncate_paragraphs
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import striptags, truncatewords
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.functional import cached_property

from ...utils.utils import get_related_items

FILE_TYPES = [
    {
        'name': 'Audio',
        'icon': 'audio',
        'extensions': ['wav', 'mp3', 'aac', 'flac'],
    },
    {
        'name': 'Excel',
        'extensions': ['xls', 'xlsx'],
        'icon': 'xls',
    },
    {
        'name': 'PDF',
        'extensions': ['pdf'],
        'icon': 'pdf',
    },
    {
        'name': 'PowerPoint',
        'extensions': ['ppt', 'pptx'],
        'icon': 'ppt',
    },
    {
        'name': 'Word document',
        'extensions': ['doc', 'docx'],
        'icon': 'doc',
    },
    {
        'name': 'Video',
        'icon': 'video',
        'extensions': ['mp4', 'mov'],
    },
    {
        'name': 'Generic document',
        'extensions': [],
        'icon': 'generic',
    },
]

ALLOWED_EXTENSIONS = []

for file_type in FILE_TYPES:
    ALLOWED_EXTENSIONS += file_type['extensions']

ALLOWED_EXTENSIONS_TEXT = ', '.join([f'.{ext}' for ext in ALLOWED_EXTENSIONS])

ICON_CHOICES = [
    (file_type['icon'], file_type['name'])
    for file_type in FILE_TYPES
]


class Resources(ContentBase):

    classifier = 'apps'

    icon = 'cms-icons/resources.png'

    # The urlconf used to power this content's views.
    urlconf = '{{ cookiecutter.package_name }}.apps.resources.urls'

    fieldsets = [
        (None, {
            'fields': ['per_page'],
        }),
    ]

    per_page = models.IntegerField(
        verbose_name='resources per page',
        default=12,
    )


class ResourceType(models.Model):
    title = models.CharField(
        max_length=32,
    )

    slug = models.SlugField(
        unique=True,
    )

    icon_override = models.CharField(
        max_length=16,
        choices=ICON_CHOICES,
        blank=True,
        null=True,
        help_text='Override the icon guessed for all files that have this type.'
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'type'

    def __str__(self):
        return self.title


class Resource(PageBase):
    page = models.ForeignKey(
        'resources.Resources'
    )

    summary = models.TextField(
        blank=True,
    )

    featured = models.BooleanField(
        default=False,
    )

    # |------------------------------------------------------------------------
    # | The resource itself
    # |------------------------------------------------------------------------

    image = ImageRefField(
        blank=True,
        null=True,
    )

    publication = models.CharField(
        'publication name',
        max_length=100,
        null=True,
        blank=True,
        help_text='The name of the journal this resource was published in.',
    )

    content = HtmlField(
        blank=True,
    )

    file = FileRefField(
        blank=True,
        null=True,
    )

    external_url = models.URLField(
        'external URL',
        blank=True,
        null=True,
    )

    # |------------------------------------------------------------------------
    # | Categorisation
    # |------------------------------------------------------------------------

    type = models.ForeignKey(
        ResourceType,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    date = models.DateTimeField(
        default=timezone.now,
    )

    class Meta:
        ordering = ['-date', 'title']

    def __str__(self):
        return self.short_title or self.title

    def clean(self):
        if not self.content and not self.file and not self.external_url:
            raise ValidationError({
                'content': 'Please provide either some page content, an attachment, or an external URL.',
            })

    def get_absolute_url(self):
        if self.content:
            return self.page.page.reverse('detail', kwargs={
                'slug': self.slug,
            })
        if self.file:
            return self.file.get_absolute_url()
        return self.external_url

    def get_summary(self, words=20):
        summary = self.summary or striptags(truncate_paragraphs(self.content, 1))

        return unescape(truncatewords(summary, words))

    @cached_property
    def file_extension(self):
        path = ''

        if self.file:
            path = self.file.file.path

        if self.external_url:
            path = self.external_url

        if path:
            # Only return an extension for known file types (e.g. don't do
            # '.asp' or '.php' for external links)
            extension = splitext(path)[1][1:].lower()
            for type_def in FILE_TYPES:
                if extension in type_def['extensions']:
                    return extension
        return None

    def render_item(self):
        return render_to_string('resources/includes/item.html', {
            'object': self,
        })

    def render_featured_item(self):
        return render_to_string('resources/includes/featured_item.html', {
            'object': self,
        })

    def get_related_resources(self, count=3):
        candidates = [Resource.objects.filter(type=self.type), Resources.objects.all()]

        return get_related_items(candidates, count, exclude=self)
