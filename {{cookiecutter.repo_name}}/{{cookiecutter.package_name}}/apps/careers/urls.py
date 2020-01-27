from django.urls import re_path

from .views import CareerDetailView, CareerListView

urlpatterns = [
    re_path(r'^$', CareerListView.as_view(), name='career_list'),
    re_path(r'^(?P<slug>[^/]+)/$', CareerDetailView.as_view(), name='career_detail'),
]
