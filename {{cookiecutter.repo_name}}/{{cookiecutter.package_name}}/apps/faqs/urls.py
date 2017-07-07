from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.FaqListView.as_view(), name='faq_list'),
    url(r'^(?P<slug>[\w-]+)/$', views.FaqView.as_view(), name='faq_detail'),
]
