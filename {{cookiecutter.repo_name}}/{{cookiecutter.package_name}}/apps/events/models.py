from html import unescape

from cms import sitemaps
from cms.apps.media.models import ImageRefField
from cms.apps.pages.models import ContentBase, PageBase
from cms.models import HtmlField
from cms.models.managers import PageBaseManager
from cms.templatetags.html import truncate_paragraphs
from django.db import models
from django.template.defaultfilters import date, striptags, truncatewords
from django.utils.timezone import now
from historylinks import shortcuts as historylinks


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
    )

    content = HtmlField()

    image = ImageRefField(
        null=True,
        blank=True,
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


historylinks.register(Event)
sitemaps.register(Event)
