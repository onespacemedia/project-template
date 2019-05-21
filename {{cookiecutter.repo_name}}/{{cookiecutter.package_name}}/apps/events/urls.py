from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.UpcomingEventListView.as_view(), name='event_list'),
    url(r'^past/$', views.PastEventListView.as_view(), name='event_list_past'),
    url(r'^(?P<slug>[^/]+)/$', views.EventDetailView.as_view(), name='event_detail'),
]
