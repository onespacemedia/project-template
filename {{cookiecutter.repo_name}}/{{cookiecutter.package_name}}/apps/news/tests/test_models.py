from datetime import timedelta

from cms.apps.pages.models import Page
from cms.models import publication_manager
from cms.plugins.moderation.models import APPROVED
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils.timezone import now
from watson import search

from ..models import (Article, Category, NewsFeed, get_default_news_feed,
                      get_default_news_page)


class TestNews(TestCase):

    def _create_objects(self):
        with search.update_index():
            self.date = now()

            content_type = ContentType.objects.get_for_model(NewsFeed)

            self.page = Page.objects.create(
                title='News Feed',
                content_type=content_type,
            )

            self.feed = NewsFeed.objects.create(
                page=self.page,
            )

            self.category = Category.objects.create(
                slug='foo'
            )

            self.article = Article.objects.create(
                page=self.feed,
                title='Foo',
                slug='foo',
                # The seconds subtraction is because of time-rounding
                # in the base publication manager.
                date=self.date - timedelta(seconds=61),
            )

            self.article.categories.add(self.category)

            self.article_2 = Article.objects.create(
                page=self.feed,
                title='Foo 2',
                slug='foo2',
                date=self.date + timedelta(days=10)
            )

            self.article_3 = Article.objects.create(
                page=self.feed,
                title='Foo 3',
                slug='foo3',
                status=APPROVED,
                date=self.date - timedelta(seconds=61),
            )

    def test_get_default_news_page_no_pages(self):
        self.assertIsNone(get_default_news_page())

    def test_get_default_news_page_with_pages(self):
        self._create_objects()
        self.assertEqual(get_default_news_page(), self.page)

    def test_get_default_news_feed_no_pages(self):
        self.assertIsNone(get_default_news_feed())

    def test_get_default_news_feed_with_pages(self):
        self._create_objects()
        self.assertEqual(get_default_news_feed(), self.feed)

    def test_article_get_permalink_for_page(self):
        self._create_objects()
        self.assertEqual(self.article._get_permalink_for_page(self.page), '/foo/')

    def test_article_get_absolute_url(self):
        self._create_objects()
        self.assertEqual(self.article.get_absolute_url(), '/foo/')

    def test_article_get_related_articles(self):
        self._create_objects()
        self.assertNotEqual(len(self.article.get_related_articles()), 0)

    def test_articlemanager_select_published(self):
        self._create_objects()

        with publication_manager.select_published(True):
            self.assertEqual(Article.objects.count(), 2)

        with publication_manager.select_published(False):
            self.assertEqual(Article.objects.count(), 3)

        # We have to manually enable the publication manager as middleware
        # isn't run during tests.
        with publication_manager.select_published(True):
            with self.settings(NEWS_APPROVAL_SYSTEM=True):
                self.assertEqual(Article.objects.count(), 1)
                self.assertEqual(len(Article.objects.all()), 1)

        # We need to generate an exception within the published block.
        with self.assertRaises(TypeError), \
             publication_manager.select_published(True):
            assert 1 / 'a'
