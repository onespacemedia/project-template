from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from reversion.admin import VersionAdmin

from ...utils.forms import UserEmailUniqueFormMixin
from .models import User


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
