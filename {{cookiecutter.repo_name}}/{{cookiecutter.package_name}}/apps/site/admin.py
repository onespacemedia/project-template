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
            'fields': ['about_title', 'about_text'],
        }),
        ('Links', {
            'fields': ['links_title'],
        }),
        ('Contact', {
            'fields': ['contact_title', 'contact_address',
                       'contact_link_text', ('contact_link_page', 'contact_link_url')],
        }),
        ('Extra links', {
            'fields': ['terms_of_use_text', ('terms_of_use_page', 'terms_of_use_url'),
                       'legal_text', ('legal_page', 'legal_url'),
                       'privacy_policy_text', ('privacy_policy_page', 'privacy_policy_url')],
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
