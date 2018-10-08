from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ContactView.as_view(), name='contact'),
    url(r'^success/$', views.ContactSuccessView.as_view(), name='contact_success'),
]
