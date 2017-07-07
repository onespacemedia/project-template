"""Models used by the CMS news app."""
from cms import sitemaps
from cms.apps.media.models import ImageRefField
from cms.apps.pages.models import ContentBase, Page
from cms.models import (HtmlField, OnlineBaseManager, PageBase,
                        PageBaseSearchAdapter)
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from historylinks import shortcuts as historylinks
from historylinks.registration import HistoryLinkAdapter


class NewsFeed(ContentBase):

    """A stream of news articles."""

    icon = 'news/img/news-feed.png'

    # The heading that the admin places this content under.
    classifier = 'syndication'

    # The urlconf used to power this content's views.
    urlconf = '{{ project_name }}.apps.news.urls'

    content_primary = HtmlField(
        'primary content',
        blank=True
    )

    per_page = models.IntegerField(
        'articles per page',
        default=5,
        blank=True,
        null=True,
    )

    def __unicode__(self):
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


class Category(PageBase):

    """A category for news articles."""

    content_primary = HtmlField(
        'primary content',
        blank=True
    )

    def _get_permalink_for_page(self, page):
        """Returns the URL for this category for the given page."""
        return page.reverse('article_category_archive', kwargs={
            'slug': self.slug,
        })

    def _get_permalinks(self):
        """Returns a dictionary of all permalinks for the given category."""
        pages = Page.objects.filter(
            id__in=Article.objects.filter(
                categories=self
            ).values_list('news_feed_id', flat=True)
        )
        return dict(
            (
                'page_{id}'.format(id=page.id), self._get_permalink_for_page(page))
            for page in pages
        )

    def __unicode__(self):
        return self.short_title or self.title

    class Meta:
        verbose_name_plural = 'categories'
        unique_together = (('slug',),)
        ordering = ('title',)


class CategoryHistoryLinkAdapter(HistoryLinkAdapter):

    """History link adapter for category models."""

    def get_permalinks(self, obj):
        """Returns all permalinks for the given category."""
        return obj._get_permalinks()


historylinks.register(Category, CategoryHistoryLinkAdapter)


class ArticleManager(OnlineBaseManager):

    """Manager for Article models."""

    def select_published(self, queryset):
        all_pages = Page.objects.filter(content_type_id=ContentType.objects.get_for_model(NewsFeed))
        published_news_feed_pages = list(Page.objects.select_published(all_pages).values_list('id', flat=True))

        queryset = super(ArticleManager, self).select_published(queryset)
        queryset = queryset.filter(
            news_feed__page__pk__in=published_news_feed_pages,
            date__lte=timezone.now().replace(second=0, microsecond=0),
        )
        if getattr(settings, 'NEWS_APPROVAL_SYSTEM', False):
            queryset = queryset.filter(
                status='approved'
            )
        return queryset


STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('submitted', 'Submitted for approval'),
    ('approved', 'Approved')
]


class Article(PageBase):

    """A news article."""

    objects = ArticleManager()

    news_feed = models.ForeignKey(
        NewsFeed,
        null=True,
        blank=False,
    )

    date = models.DateTimeField(
        db_index=True,
        default=timezone.now,
    )

    image = ImageRefField(
        blank=True,
        null=True,
    )

    content = HtmlField()

    summary = models.TextField(
        blank=True,
    )

    categories = models.ManyToManyField(
        Category,
        blank=True,
    )

    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default='draft'
    )

    def _get_permalink_for_page(self, page):
        """Returns the URL of this article for the given news feed page."""
        return page.reverse('article_detail', kwargs={
            'slug': self.slug,
        })

    def get_absolute_url(self):
        """Returns the URL of the article."""
        return self._get_permalink_for_page(self.news_feed.page)

    def __unicode__(self):
        return self.short_title or self.title

    class Meta:
        unique_together = (('news_feed', 'date', 'slug',),)
        ordering = ('-date',)
        permissions = (
            ('can_approve_articles', 'Can approve articles'),
        )


historylinks.register(Article)
sitemaps.register(Article)
