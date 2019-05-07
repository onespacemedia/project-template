from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ResourceListView.as_view(), name='list'),
    url(r'^(?P<slug>[^/]+)/$', views.ResourceDetailView.as_view(), name='detail')
]
