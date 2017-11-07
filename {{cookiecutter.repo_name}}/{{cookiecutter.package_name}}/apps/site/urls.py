from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'thumbnail/(?P<pk>\d+)/(?P<width>\d+|auto)/(?P<height>\d+|auto)/(?P<format>source|jpg|png|webp)/(?P<crop>[^/]+)/', views.ImageView.as_view(), name='thumbnail'),
]
