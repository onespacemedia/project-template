from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from social_django.models import Association, Nonce, UserSocialAuth

from ...utils.forms import UserEmailUniqueFormMixin
from .models import Footer, FooterLink, Header, HeaderLink


class UserCreationAdminForm(UserEmailUniqueFormMixin, UserCreationForm):
    '''Like UserCreationForm, but forces case-insensitivity on emails.'''
    pass


class UserAdminForm(UserEmailUniqueFormMixin, UserChangeForm):
    '''Like UserChangeForm, but forces case-insensitivity on emails.'''
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin, VersionAdmin):
    add_form = UserCreationAdminForm
    form = UserAdminForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {
            'fields': ('email', 'password'),
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined',),
        }),
    )

    list_display = ['get_first_name', 'get_last_name', 'email', 'is_active', 'is_staff']
    ordering = ['last_name', 'first_name', 'email']
    readonly_fields = ['date_joined']

    def get_first_name(self, obj):
        return obj.first_name or '(None)'
    get_first_name.short_description = 'First name'
    get_first_name.admin_order_field = 'first_name'

    def get_last_name(self, obj):
        return obj.last_name or '(None)'
    get_last_name.short_description = 'Last name'
    get_last_name.admin_order_field = 'last_name'


class HeaderLinkInline(SortableInlineAdminMixin, admin.TabularInline):
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


class FooterLinkInline(SortableInlineAdminMixin, admin.TabularInline):
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
