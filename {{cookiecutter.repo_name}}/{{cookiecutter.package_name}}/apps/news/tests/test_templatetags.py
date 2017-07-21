from cms.apps.pages.models import ContentBase, Page
from django.contrib.contenttypes.models import ContentType
from django.template import VariableDoesNotExist
from django.test import TestCase
from django.utils.timezone import now
from watson import search

from ..models import Article, Category, NewsFeed
from ..templatetags.news import (get_article_archive_url, get_article_url,
                                 get_category_url, get_latest_news_articles,
                                 get_page_from_context, page_context,
                                 takes_article_page, takes_current_page)


class TestPageContent(ContentBase):
    pass


class Object(object):
    pass


class NewsTest(TestCase):

    def setUp(self):
        with search.update_index():
            content_type = ContentType.objects.get_for_model(TestPageContent)

            self.homepage = Page.objects.create(
                title='Homepage',
                slug='homepage',
                content_type=content_type,
            )

            TestPageContent.objects.create(
                page=self.homepage,
            )

    def _create_feed_article(self):
        self.date = now()
        self.date_str = '/{}/{}/{}'.format(
            self.date.strftime('%Y'),
            self.date.strftime('%b').lower(),
            self.date.strftime('%d').lstrip('0'),
        )

        # Create a NewsFeed page.
        with search.update_index():
            content_type = ContentType.objects.get_for_model(NewsFeed)

            self.page = Page.objects.create(
                title='News Feed',
                slug='news',
                parent=self.homepage,
                content_type=content_type,
            )

            self.feed = NewsFeed.objects.create(
                page=self.page,
            )

            self.category = Category.objects.create(
                slug='foo'
            )

            self.category1 = Category.objects.create(
                slug='bar'
            )

        # Create an Article.
        self.article = Article.objects.create(
            news_feed=self.feed,
            title='Article',
            slug='foo',
            date=self.date,
        )

        self.article.categories.add(self.category)

        self.article1 = Article.objects.create(
            news_feed=self.feed,
            title='Article1',
            slug='foo1',
            date=self.date,
        )

        self.article1.categories.add(self.category)

        self.article2 = Article.objects.create(
            news_feed=self.feed,
            title='Article2',
            slug='foo2',
            date=self.date,
        )

        self.article2.categories.add(self.category1)

        self.article3 = Article.objects.create(
            news_feed=self.feed,
            title='Article3',
            slug='foo3',
            date=self.date,
        )

        self.article3.categories.add(self.category1)

        self.article4 = Article.objects.create(
            news_feed=self.feed,
            title='Article4',
            slug='foo4',
            date=self.date,
        )

        self.article4.categories.add(self.category)

        self.article5 = Article.objects.create(
            news_feed=self.feed,
            title='Article5',
            slug='foo5',
            date=self.date,
        )

        self.article5.categories.add(self.category)

        self.article6 = Article.objects.create(
            news_feed=self.feed,
            title='Article6',
            slug='foo6',
            date=self.date,
        )

        self.article6.categories.add(self.category1)

        self.article7 = Article.objects.create(
            news_feed=self.feed,
            title='Article7',
            slug='foo7',
            date=self.date,
        )

        self.article7.categories.add(self.category1)


    def test_page_context(self):
        def inner_function(context):
            return context

        initial_data = {
            'request': {},
            'pages': {},
            'page': {}
        }

        context = page_context(inner_function)(initial_data)

        self.assertDictEqual(context, initial_data)

    def test_get_page_from_context(self):
        # This might seem odd, but remember that we are in the News app, we're
        # trying to get the NewsFeed, not just the current page.

        context = {}
        kwargs = {}

        self.assertIsNone(get_page_from_context(context, kwargs))

        kwargs['page'] = self.homepage.pk

        self.assertIsNone(get_page_from_context(context, kwargs))

        del kwargs['page']
        context['page'] = self.homepage.pk
        self.assertIsNone(get_page_from_context(context, kwargs))

        del context['page']
        context['pages'] = Object()
        context['pages'].current = self.homepage.pk
        self.assertIsNone(get_page_from_context(context, kwargs))

    def test_takes_current_page(self):
        def inner_function(context, page):
            return page

        with self.assertRaises(VariableDoesNotExist):
            takes_current_page(inner_function)({})

        # Create a NewsFeed page.
        with search.update_index():
            content_type = ContentType.objects.get_for_model(NewsFeed)

            self.page = Page.objects.create(
                title='News Feed',
                parent=self.homepage,
                content_type=content_type,
            )

            self.feed = NewsFeed.objects.create(
                page=self.page,
            )

        self.assertEqual(takes_current_page(inner_function)({}), self.page)

    def test_takes_article_page(self):
        def inner_function(context, article, page):
            self.assertEqual(context, {})
            self.assertEqual(article, self.article)
            self.assertEqual(page, self.page)
            return article

        self._create_feed_article()

        takes_article_page(inner_function)({}, self.article)

    def test_article_url(self):
        self._create_feed_article()

        url = get_article_url({}, self.article, page=self.page)
        self.assertEqual(url, '/news/foo/')

    def test_article_archive_url(self):
        self._create_feed_article()
        archive_url = get_article_archive_url({'request': {}}, page=self.page)
        self.assertEqual(archive_url, '/news/')

    def test_category_url(self):
        self._create_feed_article()
        self.assertEqual(get_category_url({}, self.category, page=self.page), '/news/category/foo/')

    def test_latest_news_articles(self):
        self._create_feed_article()
        articles = get_latest_news_articles({}, count=4)
        self.assertEqual(len(articles), 4)
        articles = get_latest_news_articles({}, count=9)
        self.assertEqual(len(articles), 8)

    def test_related_articles(self):
        self._create_feed_article()
        articles = get_latest_news_articles({'article':self.article}, count=3)
        self.assertEqual(len(articles), 3)
        articles = get_latest_news_articles({'article':self.article}, count=6)
        self.assertEqual(len(articles), 6)
