"""Views used by the CMS news app."""

from bs4 import BeautifulSoup
from cms.html import process as process_html
from cms.views import SearchMetaDetailMixin
from django.http import HttpResponse
from django.utils.feedgenerator import DefaultFeed
from django.views.generic import DetailView, ListView
from django.views.generic.list import BaseListView

from ...utils.utils import url_from_path
from .models import Article, Category


class ArticleMixin:
    model = Article

    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_list = Category.objects.filter(
            article__page__page=self.request.pages.current
        ).distinct()
        context['category_list'] = category_list

        return context


class ArticleListMixin(ArticleMixin):
    make_object_list = True

    allow_empty = True

    context_object_name = 'article_list'

    def get_paginate_by(self, queryset):
        return self.request.pages.current.content.per_page

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'categories',
        ).select_related(
            'image',
            'card_image',
        ).filter(
            page__page=self.request.pages.current,
        ).order_by(
            '-date'
        )


class ArticleArchiveView(ArticleListMixin, ListView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.featured_article = None

    def dispatch(self, request, *args, **kwargs):
        candidates = Article.objects.filter(featured=True)
        if candidates.exists():
            self.featured_article = candidates[:1].get()

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.featured_article:
            return super().get_queryset().exclude(id=self.featured_article.id)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['featured_article'] = self.featured_article

        return context


class ArticleFeedView(ArticleListMixin, BaseListView):

    def process_rss(self, text):
        """Processes CMS content into RSS format."""
        html = process_html(text)

        # RSS has certain requirements: iframes are not allowed, image references
        # must be absolute and style attributes are forbidden.
        soup = BeautifulSoup(html, 'html.parser')
        for element in soup.find_all():
            # Remove inline CSS (common from pasting from Word or Google Docs)
            if element.has_attr('style'):
                del element.attrs['style']

            # Make local image references absolute.
            if element.name == 'img':
                if element.has_attr('src') and element['src'].startswith('/'):
                    element['src'] = url_from_path(element['src'])

            # Remove iframe elements.
            if element.name == 'iframe':
                # No src= should not cause an exception.
                if element.has_attr('src'):
                    element.name = 'a'
                    element['href'] = element['src']
                    element.string = '[Embedded media]'
                    del element['src']
                else:
                    replacement = '[Embedded media]'
                    element.replace_with(replacement)

            # Add absolute path internal link starting with "/".
            if element.name == 'a' and element.has_attr('href'):
                element_href_value = element['href']
                if element_href_value.startswith('/') and not element_href_value.startswith('//'):
                    element['href'] = url_from_path(element_href_value)
        html = str(soup)

        return str(html)

    def get(self, request, *args, **kwargs):
        """Generates the RSS feed."""
        page = request.pages.current

        # Write the feed headers.
        feed = DefaultFeed(
            title=page.title,
            link=url_from_path(page.get_absolute_url()),
            description=page.meta_description,
        )

        # Write the feed items.
        for article in self.get_queryset()[:30]:
            feed.add_item(
                title=article.title,
                link=url_from_path(article.get_absolute_url()),
                description=self.process_rss(article.content),
                pubdate=article.date,
            )

        # Write the response.
        content = feed.writeString('utf-8')
        response = HttpResponse(content)
        response['Content-Type'] = feed.mime_type

        return response


class ArticleDetailView(ArticleMixin, SearchMetaDetailMixin, DetailView):
    pass
