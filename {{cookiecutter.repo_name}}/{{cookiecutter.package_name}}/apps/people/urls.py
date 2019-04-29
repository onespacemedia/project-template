from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.PersonListView.as_view(), name='person_list'),
    url(r'^(?P<slug>[^/]+)/$', views.PersonView.as_view(), name='person_detail')
]
