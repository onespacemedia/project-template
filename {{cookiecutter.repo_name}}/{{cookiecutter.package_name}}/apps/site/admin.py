from django.contrib import admin
from social_django.models import Association, Nonce, UserSocialAuth
from suit.admin import SortableStackedInline

from .models import Footer, FooterLink, Header, HeaderLink


class HeaderLinkInline(SortableStackedInline):
    model = HeaderLink
    extra = 0


@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    inlines = [HeaderLinkInline]

    class Media:
        css = {
            'all': ['/static/css/admin-sections.css'],
        }

    def has_add_permission(self, request):
        return not Header.objects.count()


class FooterLinkInline(SortableStackedInline):
    model = FooterLink
    extra = 0


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    inlines = [FooterLinkInline]

    fieldsets = [
        ('About', {
            'fields': ['text'],
        }),
        ('Extra links', {
            'fields': [('terms_link_page', 'terms_link_url'),
                       ('legal_link_page', 'legal_link_url'),
                       ('privacy_link_page', 'privacy_link_url'), ],
        }),
    ]

    class Media:
        css = {
            'all': ['/static/css/admin-sections.css'],
        }

    def has_add_permission(self, request):
        return not Footer.objects.count()


# Unregister python social auth models (not really needed or useful).
for model in [Association, Nonce, UserSocialAuth]:
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass
