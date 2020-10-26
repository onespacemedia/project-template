from django.http import HttpResponse
from django.urls import re_path
from django.views import View


class TestView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(f'Response for {request.path_info}')


urlpatterns = [
    re_path(r'^$', TestView.as_view()),
    re_path(r'/regex-test-cases/(?P<slug>[^/]+)/$', TestView.as_view()),
    re_path(r'/test-cases/normal-redirect/$', TestView.as_view()),
    re_path(r'/test-cases/unslashed-redirect/$', TestView.as_view()),
]
