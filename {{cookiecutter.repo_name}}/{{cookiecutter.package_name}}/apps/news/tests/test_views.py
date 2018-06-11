from bs4 import BeautifulSoup
from cms.apps.pages.middleware import RequestPageManager
from cms.apps.pages.models import Page
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory, TestCase
from django.utils.timezone import now
from django.views import generic
from watson import search

from ....utils.utils import url_from_path
from ..models import Article, Category, NewsFeed
from ..views import ArticleDetailView, ArticleFeedView, ArticleListMixin


class TestView(ArticleListMixin, generic.ListView):
    pass


class TestViews(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        with search.update_index():
            self.date = now()
            self.date_str = '/{}/{}/{}'.format(
                self.date.strftime('%Y'),
                self.date.strftime('%b').lower(),
                self.date.strftime('%d').lstrip('0'),
            )

            content_type = ContentType.objects.get_for_model(NewsFeed)

            self.page = Page.objects.create(
                title='News Feed',
                slug='news',
                content_type=content_type,
            )

            self.feed = NewsFeed.objects.create(
                page=self.page,
            )

            self.article = Article.objects.create(
                page=self.feed,
                title='Foo',
                slug='foo',
                content=r'<p>Some links in this article below</p>\r\n<p><a href="/newfeedpage/" title="Valid news feedpage">/newfeedpage/</a></p>\r\n<p><a href="newfeedpage/" title="Invalid news feedpage">newfeedpage</a></p>\r\n<p></p>\r\n<p>iframe below</p>\r\n<p><iframe src="https://www.w3schools.com"></iframe></p>\r\n<p>an_image below</p>\r\n<p><img src="/r/16-2/" alt="events_02" title="events_02" /></p>',
                date=self.date,
            )

            self.category = Category.objects.create(
                title='Foo',
                slug='foo'
            )
            self.article.categories.add(self.category)

    def test_articlelistmixin_get_paginate_by(self):
        view = ArticleListMixin()
        view.request = self.factory.get('/')
        view.request.pages = RequestPageManager(view.request)

        self.assertEqual(view.get_paginate_by(None), 12)

    def test_articlelistmixin_get_context_data(self):
        view = TestView()
        view.request = self.factory.get('/')
        view.request.pages = RequestPageManager(view.request)
        view.object_list = Article.objects.all()
        view.kwargs = {}

        data = view.get_context_data()

        self.assertEqual(list(data['article_list']), [self.article])
        self.assertEqual(list(data['object_list']), [self.article])
        self.assertEqual(list(data['category_list']), [self.category])
        self.assertEqual(repr(data['page_obj']), '<Page 1 of 1>')
        self.assertFalse(data['is_paginated'])

    def test_articlelistmixin_get_queryset(self):
        view = TestView()
        view.request = self.factory.get('/')
        view.request.pages = RequestPageManager(view.request)

        self.assertListEqual(list(view.get_queryset()), [self.article])

    def test_articlefeedview_get(self):
        view = ArticleFeedView()
        view.request = self.factory.get('/news/feed/')
        view.request.pages = RequestPageManager(view.request)

        get = view.get(view.request)

        content = get.content
        content = content.decode('utf-8')
        soup = BeautifulSoup(content, features="xml")
        links = soup.find_all('link')
        news_url_link = str(links[0])
        article_url_link = str(links[1])

        self.assertEqual(get.status_code, 200)
        self.assertGreater(len(content), len(self.article.content))

        # bs returns None if there is no RSS tag. This behaviour may change in future?
        self.assertIsNotNone(soup.rss)
        self.assertIsNone(soup.iframe)
        self.assertEqual(news_url_link, f'<link>{url_from_path("/")}</link>')
        self.assertEqual(article_url_link, f'<link>{url_from_path(self.article.slug)}/</link>')
        self.assertEqual(get['Content-Type'], 'application/rss+xml; charset=utf-8')

    def test_articledetailview_get_context_data(self):
        view = ArticleDetailView()
        view.request = self.factory.get('/news/foo/')
        view.request.pages = RequestPageManager(view.request)
        view.object = self.article

        data = view.get_context_data()

        self.assertEqual(data['meta_description'], '')
        self.assertEqual(data['robots_follow'], True)
        self.assertEqual(list(data['category_list']), [self.category])
        self.assertEqual(data['robots_index'], True)
        self.assertEqual(data['title'], 'Foo')
        self.assertEqual(data['object'], self.article)
        self.assertEqual(data['robots_archive'], True)
        self.assertEqual(data['header'], 'Foo')
        self.assertEqual(data['article'], self.article)
        self.assertEqual(data['view'], view)
