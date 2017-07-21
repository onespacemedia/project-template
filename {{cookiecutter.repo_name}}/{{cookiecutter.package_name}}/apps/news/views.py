"""Views used by the CMS news app."""

from cms.html import process as process_html
from cms.views import SearchMetaDetailMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
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
            'image'
        ).filter(
            news_feed__page=self.request.pages.current,
        ).order_by(
            '-date'
        )


class ArticleArchiveView(ArticleListMixin, ListView):
    pass


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

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)

        # Get the next article.
        try:
            next_article = self.object.get_next_by_date()
        except Article.DoesNotExist:
            next_article = None

        # Get the previous article.
        try:
            prev_article = self.object.get_previous_by_date()
        except Article.DoesNotExist:
            prev_article = None

        context['next_article'] = next_article
        context['prev_article'] = prev_article

        return context


class ArticleCategoryArchiveView(SearchMetaDetailMixin, ArticleArchiveView):
    template_name = 'news/article_category_archive.html'

    def get_queryset(self):
        """Returns the queryset filtered by category."""
        return super(ArticleCategoryArchiveView, self).get_queryset().filter(
            categories=self.object,
        )

    def get_context_data(self, **kwargs):
        """Adds the category to the context."""
        context = super(ArticleCategoryArchiveView, self).get_context_data(**kwargs)
        context['category'] = self.object

        return context

    def dispatch(self, request, *args, **kwargs):
        """Parses the category from the request."""
        self.object = get_object_or_404(
            Category,
            slug=kwargs['slug'],
        )

        return super(ArticleCategoryArchiveView, self).dispatch(request, *args, **kwargs)
