"""URL config for {{cookiecutter.repo_name}} project."""

from cms.forms import CMSPasswordChangeForm
from cms.sitemaps import registered_sitemaps
from cms.views import TextTemplateView
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import generic

{% if cookiecutter.sections == 'no' %}# {% endif %}from .apps.sections.models import sections_js
from {{cookiecutter.package_name}}.utils.views import FrontendView

admin.autodiscover()


urlpatterns = [

    # Admin URLs.
    url(r'^admin/password_change/$', 'django.contrib.auth.views.password_change',
        {'password_change_form': CMSPasswordChangeForm}, name='password_change'),
    url(r'^admin/password_change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r"^admin/", include(admin.site.urls)),
    url(r'^admin/', include('social.apps.django_app.urls', namespace='social')),
    {% if cookiecutter.sections == 'no' %}# {% endif %}url(r'^admin/pages/page/sections.js$', sections_js, name="admin_sections_js"),

    # Permalink redirection service.
    url(r"^r/(?P<content_type_id>\d+)-(?P<object_id>[^/]+)/$", "django.contrib.contenttypes.views.shortcut", name="permalink_redirect"),

    # Google sitemap service.
    url(r"^sitemap.xml$", "django.contrib.sitemaps.views.index", {"sitemaps": registered_sitemaps}),
    url(r"^sitemap-(?P<section>.+)\.xml$", "django.contrib.sitemaps.views.sitemap", {"sitemaps": registered_sitemaps}),

    # Basic robots.txt.
    url(r"^robots.txt$", TextTemplateView.as_view(template_name="robots.txt")),

    # There's no favicon here!
    url(r"^favicon.ico$", generic.RedirectView.as_view(permanent=True)),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) + static(
    settings.NODE_MODULES_URL, document_root=settings.NODE_MODULES_ROOT
)


if settings.DEBUG:
    urlpatterns += [
        url(r"^404/$", generic.TemplateView.as_view(template_name="404.html")),
        url(r"^500/$", generic.TemplateView.as_view(template_name="500.html")),
        url(r'^frontend/$', FrontendView.as_view()),
        url(r'^frontend/(?P<slug>[\w-]+)/$', FrontendView.as_view())
    ]


handler500 = "cms.views.handler500"
