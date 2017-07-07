from cms import sitemaps
from cms.apps.media.models import ImageRefField
from cms.apps.pages.models import ContentBase, PageBase
from cms.models import HtmlField
from django.db import models
from django.template.defaultfilters import date
from historylinks import shortcuts as historylinks


class Events(ContentBase):

    classifier = 'apps'
    urlconf = '{{ project_name }}.apps.events.urls'

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


class Event(PageBase):

    page = models.ForeignKey(
        Events,
    )

    start_date = models.DateField()

    end_date = models.DateField()

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
        if self.page:
            return self.page.page.reverse('event_detail', kwargs={
                'slug': self.slug,
            })

    def get_summary(self):
        return self.summary

    @property
    def date(self):
        date_string = '{}'.format(date(self.start_date, 'j F Y'))

        if self.start_date != self.end_date:
            date_string += ' - {}'.format(date(self.end_date, 'j F Y'))

        return date_string

historylinks.register(Event)
sitemaps.register(Event)
