"""Models used by the CMS news app."""
import json
from html import unescape

from cms import sitemaps
from cms.apps.media.models import ImageRefField
from cms.apps.pages.models import ContentBase, Page
from cms.models import HtmlField, OnlineBaseManager, PageBase
from cms.plugins.moderation.models import APPROVED, DRAFT, STATUS_CHOICES
from cms.templatetags.html import truncate_paragraphs
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import striptags, truncatewords
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from historylinks import shortcuts as historylinks
from reversion.models import Version

from ...utils.utils import (ORGANISATION_SCHEMA, get_related_items,
                            schema_image, url_from_path)


class NewsFeed(ContentBase):

    """A stream of news articles."""
    classifier = 'apps'
    icon = 'cms-icons/news.png'

    # The urlconf used to power this content's views.
    urlconf = '{{ cookiecutter.package_name }}.apps.news.urls'
    fieldsets = [
        (None, {
            'fields': ['per_page', 'call_to_action'],
        }),
        ('Hero', {
            'fields': ['hero_kicker', 'hero_title'],
        }),
    ]

    hero_kicker = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='If this is left blank it will use the page title',
    )

    hero_title = models.CharField(
        max_length=255,
    )

    per_page = models.IntegerField(
        verbose_name='Articles per page',
        default=12,
    )

    call_to_action = models.ForeignKey(
        'components.CallToAction',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.page.title


def get_default_news_page():
    """Returns the default news page."""
    try:
        return Page.objects.filter(
            content_type=ContentType.objects.get_for_model(NewsFeed),
        ).order_by('left')[0]
    except IndexError:
        return None


def get_default_news_feed():
    """Returns the default news feed for the site."""
    page = get_default_news_page()
    if page:
        return page.content
    return None


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


class ArticleManager(OnlineBaseManager):
    """Manager for Article models."""

    def select_published(self, queryset):
        all_pages = Page.objects.filter(content_type_id=ContentType.objects.get_for_model(NewsFeed))
        published_news_feed_pages = list(Page.objects.select_published(all_pages).values_list('id', flat=True))

        queryset = super(ArticleManager, self).select_published(queryset)
        queryset = queryset.filter(
            page__page__pk__in=published_news_feed_pages,
            date__lte=timezone.now().replace(second=0, microsecond=0),
        )
        if getattr(settings, 'NEWS_APPROVAL_SYSTEM', False):
            queryset = queryset.filter(
                status=APPROVED
            )
        return queryset


class Article(PageBase):
    """A news article."""

    objects = ArticleManager()

    page = models.ForeignKey(
        'news.NewsFeed',
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        verbose_name='News feed'
    )

    featured = models.BooleanField(
        default=False,
    )

    date = models.DateTimeField(
        db_index=True,
        default=timezone.now,
    )

    image = ImageRefField(
        blank=True,
        null=True,
    )

    card_image = ImageRefField(
        blank=True,
        null=True,
        help_text="By default the card will try and use the main image, if it doesn't look right you can override it here.",
    )

    content = HtmlField()

    summary = models.TextField(
        blank=True,
    )

    call_to_action = models.ForeignKey(
        'components.CallToAction',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="By default the call to action will be the same as the news feed. You can override it for a specific article here."
    )

    categories = models.ManyToManyField(
        'news.Category',
        blank=True,
    )
{% if cookiecutter.people == 'yes' %}    author = models.ForeignKey(
        'people.Person',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    ){% endif %}
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default=DRAFT,
    )

    class Meta:
        unique_together = [['page', 'slug']]
        ordering = ['-date']
        permissions = [
            ('can_approve_articles', 'Can approve articles'),
        ]

    def __str__(self):
        return self.short_title or self.title

    def _get_permalink_for_page(self, page):
        """Returns the URL of this article for the given news feed page."""
        return page.reverse('article_detail', kwargs={
            'slug': self.slug,
        })

    def get_absolute_url(self):
        """Returns the URL of the article."""
        return self._get_permalink_for_page(self.page.page)

    def get_related_articles(self, count=3):
        candidate_querysets = [
            Article.objects.filter(categories__in=self.categories.all()),
            Article.objects.all(),
        ]
        return get_related_items(candidate_querysets, count=count, exclude=self)

    def get_summary(self, words=20):
        summary = self.summary or striptags(truncate_paragraphs(self.content, 1))

        return unescape(truncatewords(summary, words))

    @property
    def last_modified(self):
        version = Version.objects.get_for_object(self).first()

        if version:
            return version.revision.date_created

    def render_card(self):
        return render_to_string('news/includes/card.html', {
            'object': self,
        })

    def render_featured_card(self):
        return render_to_string('news/includes/featured_card.html', {
            'object': self,
        })

    @property
    def tagless_content(self):
        return strip_tags(self.content)

    @cached_property
    def word_count(self):
        return len(self.tagless_content.split(' '))

    def schema(self):
        schema = {
            '@context': 'http://schema.org',
            '@type': 'Article',
            'author': {% if cookiecutter.people == 'yes' %}str(self.author) or {% endif %}settings.SITE_NAME,
            'publisher': ORGANISATION_SCHEMA,
            'name': self.title,
            'headline': self.title,
            'text': self.summary or '',
            'articleBody': self.tagless_content,
            'keywords': ','.join([x.title for x in self.categories.all()]),
            'inLanguage': {
                'type': 'Language',
                'name': ['English']
            },
            'mainEntityOfPage': url_from_path(self.get_absolute_url()),
            'dateCreated': self.date.isoformat(),
            'dateModified': self.last_modified.isoformat() or self.date.isoformat(),
            'datePublished': self.date.isoformat(),
            'wordCount': self.word_count
        }

        if self.image:
            schema['image'] = schema_image(self.image)
        if self.card_image:
            schema['thumbnailUrl'] = schema_image(self.card_image)

        return mark_safe(json.dumps(schema))


historylinks.register(Article)
sitemaps.register(Article)
