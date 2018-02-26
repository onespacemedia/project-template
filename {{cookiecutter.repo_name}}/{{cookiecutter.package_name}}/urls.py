from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.contenttypes import views as contenttypes_views
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views import generic
from django.views.static import serve


admin.autodiscover()


urlpatterns = [
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'cmspages': CMSSitemap}}),

    # Admin URLs.
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include('social_django.urls', namespace='social')),

    # Basic robots.txt.
    url(r'^robots.txt$', generic.TemplateView.as_view(template_name='robots.txt', content_type="text/plain; charset=utf-8")),

    # Permalink redirection service.
    url(r'^r/(?P<content_type_id>\d+)-(?P<object_id>[^/]+)/$', contenttypes_views.shortcut, name='permalink_redirect'),

    # There's no favicon here!
    url(r'^favicon.ico$', generic.RedirectView.as_view(permanent=True)),
]

if settings.DEBUG:
    from .utils.views import FrontendView

    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^404/$', generic.TemplateView.as_view(template_name='404.html')),
        url(r'^500/$', generic.TemplateView.as_view(template_name='500.html')),
        url(r'^frontend/$', FrontendView.as_view()),
        url(r'^frontend/(?P<slug>[\w-]+)/$', FrontendView.as_view())
    ] + staticfiles_urlpatterns() + urlpatterns

urlpatterns += i18n_patterns(
    url(r'^', include('cms.urls')),
)
