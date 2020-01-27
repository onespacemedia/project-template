from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.ResourceListView.as_view(), name='list'),
    re_path(r'^(?P<slug>[^/]+)/$', views.ResourceDetailView.as_view(), name='detail')
]
