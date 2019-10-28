import logging
import sys

from cms.sitemaps import registered_sitemaps
from cms.views import TextTemplateView
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.contenttypes import views as contenttypes_views
from django.contrib.sitemaps import views as sitemaps_views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import render
from django.views import generic

from .apps.users import auth_views as reset_views

{% if cookiecutter.sections == 'no' %}# {% endif %}from .apps.sections.models import sections_js
from .utils.views import FrontendView

admin.autodiscover()


urlpatterns = [

    # Admin URLs.
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include('social_django.urls', namespace='social')),
    {% if cookiecutter.sections == 'no' %}# {% endif %}url(r'^admin/pages/page/sections.js$', sections_js, name='admin_sections_js'),
    url(r'^admin/reset-password/$', reset_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^admin/reset-password/sent/$', reset_views.PasswordResetSentView.as_view(), name='password_reset_sent'),
    url(
        r'^admin/reset-password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        reset_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    # Site URLs
    url(r'^assets/', include('django_lazy_image.urls', namespace='assets')),

    # Jet URLs
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),

    # Permalink redirection service.
    url(r'^r/(?P<content_type_id>\d+)-(?P<object_id>[^/]+)/$', contenttypes_views.shortcut, name='permalink_redirect'),

    # Google sitemap service.
    url(r'^sitemap.xml$', sitemaps_views.index, {'sitemaps': registered_sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemaps_views.sitemap, {'sitemaps': registered_sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Basic robots.txt.
    url(r'^robots.txt$', TextTemplateView.as_view(template_name='robots.txt')),

    # There's no favicon here!
    url(r'^favicon.ico$', generic.RedirectView.as_view(url=staticfiles_storage.url('favicons/favicon.ico'), permanent=True)),
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
