import logging
import sys

from cms.sitemaps import registered_sitemaps
from cms.views import TextTemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.contenttypes import views as contenttypes_views
from django.contrib.sitemaps import views as sitemaps_views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, re_path
from django.shortcuts import render
from django.views import generic

{% if cookiecutter.sections == 'no' %}# {% endif %}from .apps.sections.models import sections_js
from .utils.views import FrontendView

admin.autodiscover()


urlpatterns = [

    # Admin URLs.
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^admin/', include('social_django.urls', namespace='social')),
    re_path(r'^admin/', include('{{ cookiecutter.package_name }}.apps.users.urls')),
    {% if cookiecutter.sections == 'no' %}# {% endif %}re_path(r'^admin/pages/page/sections.js$', sections_js, name='admin_sections_js'),

    # Site URLs
    re_path(r'^assets/', include(('django_lazy_image.urls', 'lazy_image'), namespace='assets')),

    # Jet URLs
    re_path(r'^jet/', include('jet.urls', 'jet')),
    re_path(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),

    # Permalink redirection service.
    re_path(r'^r/(?P<content_type_id>\d+)-(?P<object_id>[^/]+)/$', contenttypes_views.shortcut, name='permalink_redirect'),

    # Google sitemap service.
    re_path(r'^sitemap.xml$', sitemaps_views.index, {'sitemaps': registered_sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'^sitemap-(?P<section>.+)\.xml$', sitemaps_views.sitemap, {'sitemaps': registered_sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Basic robots.txt.
    re_path(r'^robots.txt$', TextTemplateView.as_view(template_name='robots.txt')),

    # There's no favicon here!
    re_path(r'^favicon.ico$', generic.RedirectView.as_view(url=staticfiles_storage.url('favicons/favicon.ico'), permanent=True)),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)


if settings.DEBUG:
    urlpatterns += [
        url(r'^404/$', generic.TemplateView.as_view(template_name='404.html')),
        url(r'^500/$', generic.TemplateView.as_view(template_name='500.html')),
        url(r'^frontend/$', FrontendView.as_view()),
        url(r'^frontend/(?P<slug>[\w-]+)/$', FrontendView.as_view())
    ]


def handler500(request):
    '''Renders a nicer error page and sends errors to Rollbar.'''
    import traceback

    logger = logging.getLogger('{{ cookiecutter.package_name }}')

    type_, value, _ = sys.exc_info()

    logger.error(
        '%s: %s',
        type_.__name__,
        value,
        exc_info=True,
        extra={
            'traceback': ''.join(traceback.format_stack()),
        }
    )

    response = render(request, "500.html", {})
    response.status_code = 500
    return response
