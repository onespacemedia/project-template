"""Views used by the CMS news app."""

from cms.html import process as process_html
from cms.views import SearchMetaDetailMixin
from django.http import HttpResponse
from django.utils.feedgenerator import DefaultFeed
from django.views.generic import DetailView, ListView
from django.views.generic.list import BaseListView

from .models import Article, Category


class ArticleMixin(object):
    model = Article

    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleMixin, self).get_context_data(**kwargs)
        category_list = Category.objects.filter(
            article__news_feed__page=self.request.pages.current
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
        return super(ArticleListMixin, self).get_queryset().prefetch_related(
            'categories',
        ).select_related(
            'image',
            'card_image',
        ).filter(
            news_feed__page=self.request.pages.current,
        ).order_by(
            '-date'
        )


class ArticleArchiveView(ArticleListMixin, ListView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.featured_article = None

    def dispatch(self, request, *args, **kwargs):
        self.featured_article = Article.objects.filter(featured=True)[:1].get()

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().exclude(id=self.featured_article.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['featured_article'] = self.featured_article

        return context


class ArticleFeedView(ArticleListMixin, BaseListView):
    def get(self, request, *args, **kwargs):
        """Generates the RSS feed."""
        page = request.pages.current

        # Write the feed headers.
        feed = DefaultFeed(
            title=page.title,
            link=page.get_absolute_url(),
            description=page.meta_description,
        )

        # Write the feed items.
        for article in self.get_queryset()[:30]:
            feed.add_item(
                title=article.title,
                link=article.get_absolute_url(),
                description=process_html(
                    article.summary or article.content),
                pubdate=article.date,
            )

        # Write the response.
        content = feed.writeString('utf-8')
        response = HttpResponse(content)
        response['Content-Type'] = feed.mime_type
        response['Content-Length'] = len(content)

        return response


class ArticleDetailView(ArticleMixin, SearchMetaDetailMixin, DetailView):
    pass
