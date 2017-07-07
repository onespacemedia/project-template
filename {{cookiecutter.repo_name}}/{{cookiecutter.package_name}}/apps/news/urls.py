"""URLs used by the CMS news app."""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ArticleArchiveView.as_view(), name='article_archive'),
    url(r'^feed/$', views.ArticleFeedView.as_view(), name='article_feed'),
    url(r'^category/(?P<slug>[^/]+)/$', views.ArticleCategoryArchiveView.as_view(), name='article_category_archive'),
    url(r'^(?P<slug>[^/]+)/$', views.ArticleDetailView.as_view(), name='article_detail'),
]
