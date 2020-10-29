from django.urls import re_path

from .views import DeferredThumbnailView

urlpatterns = [
    re_path(r'defer/(?P<key>[^/]+)/$', DeferredThumbnailView.as_view(), name='deferred_image')
]
