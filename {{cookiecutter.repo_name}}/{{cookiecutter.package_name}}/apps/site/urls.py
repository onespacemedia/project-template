from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'thumbnail/(?P<pk>\d+)/(?P<width>\d+|auto)/(?P<height>\d+|auto)/(?P<format>source|jpg|png|webp)/(?P<crop>[^/]+)/', views.ImageView.as_view(), name='thumbnail'),
]
