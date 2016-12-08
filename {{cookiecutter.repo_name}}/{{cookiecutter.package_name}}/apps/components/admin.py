from django.contrib import admin
from django.core.urlresolvers import reverse

from ...utils.admin import UsedOnAdminMixin
from .models import CallToAction


# @admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin, UsedOnAdminMixin):
    list_display = ['title', 'pages_used_on']
