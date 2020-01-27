from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.PersonListView.as_view(), name='person_list'),
    re_path(r'^(?P<slug>[^/]+)/$', views.PersonView.as_view(), name='person_detail')
]
