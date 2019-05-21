import json
from html import unescape

from cms import sitemaps
from cms.apps.media.models import ImageRefField
from cms.apps.pages.models import ContentBase, PageBase
from cms.models import HtmlField
from cms.models.managers import PageBaseManager
from cms.templatetags.html import truncate_paragraphs
from django.db import models
from django.template.defaultfilters import date, striptags, truncatewords
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from historylinks import shortcuts as historylinks

from ...utils.utils import schema_image, url_from_path


class Events(ContentBase):

    classifier = 'apps'
    icon = 'cms-icons/events.png'
    urlconf = '{{ cookiecutter.package_name }}.apps.events.urls'

    hero_title_past = models.CharField(
        max_length=255,
        verbose_name='past events title',
        blank=True,
        null=True,
    )

    per_page = models.PositiveIntegerField(
        'events per page',
        default=10,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.page.title


class Category(models.Model):
    title = models.CharField(
        max_length=50,
    )

    slug = models.SlugField(
        unique=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['order']

    def __str__(self):
        return self.title


class EventQueryset(models.QuerySet):

    def select_upcoming(self):
        return self.filter(end_date__gte=now().date())

    def select_past(self):
        return self.filter(end_date__lt=now().date())


class Event(PageBase):

    objects = PageBaseManager.from_queryset(EventQueryset)()

    page = models.ForeignKey(
        Events,
        on_delete=models.PROTECT,
    )

    featured = models.BooleanField(
        default=False,
    )

    start_date = models.DateField()

    end_date = models.DateField()

    summary = models.TextField(
        blank=True,
        null=True,
    )

    content = HtmlField()

    image = ImageRefField(
        null=True,
        blank=True,
    )

    card_image = ImageRefField(
        blank=True,
        null=True,
        help_text="By default the card will try and use the main image, if it doesn't look right you can override it here.",
    )

    categories = models.ManyToManyField(
        'events.Category',
        blank=True,
    )

    class Meta:
        ordering = ['start_date']
        unique_together = [['page', 'slug']]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.page.page.reverse('event_detail', kwargs={
            'slug': self.slug,
        })

    def get_summary(self, words=20):
        summary = self.summary or striptags(truncate_paragraphs(self.content, 1))

        return unescape(truncatewords(summary, words))

    @property
    def date(self):
        date_string = '{}'.format(date(self.start_date, 'j F Y'))

        if self.start_date != self.end_date:
            date_string += ' - {}'.format(date(self.end_date, 'j F Y'))

        return date_string

    def schema(self):
        schema = {
            '@context': 'http://schema.org',
            '@type': 'Event',
            'startDate': self.start_date.isoformat(),
            'endDate': self.end_date.isoformat(),
            'description': self.summary or '',
            'name': self.title,
            'mainEntityOfPage': url_from_path(self.get_absolute_url()),
            'location': {
                '@type': 'Place',
                'name': 'Unknown',
                'address': 'Unknown'
            },
        }

        if self.image:
            schema['image'] = schema_image(self.image)

        return mark_safe(json.dumps(schema))

      def render_card(self):
        return render_to_string('events/includes/card.html', {
            'object': self,
        })

    def render_featured_card(self):
        return render_to_string('events/includes/featured_card.html', {
            'object': self,
        })


historylinks.register(Event)
sitemaps.register(Event)
