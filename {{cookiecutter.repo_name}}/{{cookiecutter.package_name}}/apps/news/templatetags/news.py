"""Template tags used by the news module."""

from functools import wraps

import jinja2
from cms.apps.pages.models import Page
from django import template
from django.contrib.contenttypes.models import ContentType
from django.utils.html import escape
from django_jinja import library

from ..models import Article, NewsFeed, get_default_news_page


def page_context(func):
    """Decorator for functions that pass on the current page into the next context."""

    @wraps(func)
    def do_page_context(context, *args, **kwargs):
        params = func(context, *args, **kwargs)
        params['request'] = context['request']

        if 'pages' in context:
            params['pages'] = context['pages']
        if 'page' in context:
            params['page'] = context['page']

        return params

    return do_page_context


def get_page_from_context(context, kwargs):
    """Returns the current page based on the given template context."""
    page = None

    # Resolve the page.
    if 'page' in kwargs:
        page = kwargs['page']
    elif 'page' in context:
        page = context['page']
    elif 'pages' in context:
        pages = context['pages']
        page = pages.current

    # Adapt the page.
    if isinstance(page, int):
        page = Page.objects.get(id=page)
    if page and page.content_type_id != ContentType.objects.get_for_model(NewsFeed).id:
        page = get_default_news_page()

    return page


def takes_current_page(func):
    """Decorator for template tags that require the current page."""

    @wraps(func)
    def do_takes_current_page(context, *args, **kwargs):
        page = get_page_from_context(context, kwargs)

        if not page:
            page = get_default_news_page()
        if page is None:
            raise template.VariableDoesNotExist('Could not determine the current page from the template context.')
        kwargs['page'] = page

        return func(context, *args, **kwargs)

    return do_takes_current_page


def takes_article_page(func):
    """Decorator for template tags that require a page for an article."""

    @wraps(func)
    def do_takes_article_page(context, article, *args, **kwargs):
        page = get_page_from_context(context, kwargs)

        if not page or page.id != article.news_feed_id:
            page = article.news_feed.page

        kwargs['page'] = page

        return func(context, article, *args, **kwargs)

    return do_takes_article_page


@library.global_function
@jinja2.contextfunction
@takes_article_page
def get_article_url(context, article, page):
    """Renders the URL for an article."""
    return escape(article._get_permalink_for_page(page))


@library.global_function
@jinja2.contextfunction
@takes_current_page
def get_article_archive_url(context, page):
    """Renders the URL for the current article archive."""
    return escape(page.reverse('article_archive'))


@library.global_function
@jinja2.contextfunction
@takes_current_page
def get_category_url(context, category, page):
    """Renders the URL for the given category."""
    return escape(category._get_permalink_for_page(page))


@library.global_function
@jinja2.contextfunction
def get_latest_news_articles(context, count=3, news_feed=None):
    articles = Article.objects.all()

    if news_feed:
        articles = articles.filter(news_feed=news_feed)

    return articles[:count]


@library.global_function
@jinja2.contextfunction
def get_related_articles(context, count=4):
    current_article = context['article']

    related_articles = list(Article.objects.exclude(
        pk=current_article.pk
    ).filter(
        categories__in=current_article.categories.all(),
    ).distinct()[:count])

    if len(related_articles.count()) >= count:
        return related_articles[:count]

    # If we couldn't get enough related articles, pad out the data with others.
    missing = count - len(related_articles)

    padding = Article.objects.exclude(
        pk__in=[article.pk for article in related_articles] + [current_article.pk]
    ).distinct()[:missing]

    return list(related_articles) + list(padding)
