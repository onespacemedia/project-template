from django.conf import settings
from django.contrib import admin

from .models import Setting


class SettingAdmin(admin.ModelAdmin):
    prepopulated_fields = {'key': ['name']}

    list_display = ['name', 'key']

    def get_form(self, request, obj=None, **kwargs):
        if getattr(settings, 'SETTINGS_ADMINS', None) is not None:
            if obj and request.user.username not in settings.SETTINGS_ADMINS:
                self.exclude = ['name', 'key']
                self.prepopulated_fields = {}

        return super(SettingAdmin, self).get_form(request, obj, **kwargs)

    def has_add_permission(self, request):
        if getattr(settings, 'SETTINGS_ADMINS', None) is not None:
            return request.user.username in settings.SETTINGS_ADMINS
        return super(SettingAdmin, self).has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if getattr(settings, 'SETTINGS_ADMINS', None) is not None:
            return request.user.username in settings.SETTINGS_ADMINS
        return super(SettingAdmin, self).has_delete_permission(request, obj)

    def setting_name(self, obj):
        return obj.name

    class Media:
        js = ('/static/settings/js/admin/fields.js',)


admin.site.register(Setting, SettingAdmin)
