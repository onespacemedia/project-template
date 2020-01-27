"""URLs used by the CMS news app."""

from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.ArticleArchiveView.as_view(), name='article_archive'),
    re_path(r'^feed/$', views.ArticleFeedView.as_view(), name='article_feed'),
    re_path(r'^(?P<slug>[^/]+)/$', views.ArticleDetailView.as_view(), name='article_detail'),
]
