import json

from cms import sitemaps
from cms.apps.media.models import ImageRefField
from cms.apps.pages.models import ContentBase, PageBase
from cms.models import HtmlField
from cms.models.managers import PageBaseManager
from django.db import models
from django.template.defaultfilters import date
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from historylinks import shortcuts as historylinks

from ...utils.utils import schema_image, url_from_path


class Events(ContentBase):

    classifier = 'apps'
    icon = 'cms-icons/events.png'
    urlconf = '{{ cookiecutter.package_name }}.apps.events.urls'

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
        max_length=100,
    )

    class Meta:
        verbose_name_plural = 'categories'

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

    start_date = models.DateField()

    end_date = models.DateField()

    summary = models.TextField(
        blank=True,
        null=True,
    )

    description = HtmlField()

    image = ImageRefField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.page.page.reverse('event_detail', kwargs={
            'slug': self.slug,
        })

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


historylinks.register(Event)
sitemaps.register(Event)
