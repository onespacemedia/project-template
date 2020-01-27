from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.UpcomingEventListView.as_view(), name='event_list'),
    re_path(r'^past/$', views.PastEventListView.as_view(), name='event_list_past'),
    re_path(r'^(?P<slug>[^/]+)/$', views.EventDetailView.as_view(), name='event_detail'),
]
