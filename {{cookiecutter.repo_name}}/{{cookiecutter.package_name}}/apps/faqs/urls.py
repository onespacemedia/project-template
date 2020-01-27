from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.FaqListView.as_view(), name='faq_list'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.FaqView.as_view(), name='faq_detail'),
]
