from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.ContactView.as_view(), name='contact'),
    re_path(r'^success/$', views.ContactSuccessView.as_view(), name='contact_success'),
]
