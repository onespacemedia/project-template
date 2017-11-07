from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import EmailLog, EmailTemplate


@admin.register(EmailTemplate)
class EmailTemplateAdmin(VersionAdmin):

    list_display = ['title', 'reference', 'from_email', 'reply_to', 'bcc_list', 'subject']

    suit_form_includes = [
        ('emails/previews/email_template_preview.html', '', ''),
    ]


@admin.register(EmailLog)
class EmailLogAdmin(VersionAdmin):

    list_display = ['email_template', 'to', 'from_email', 'subject', 'timestamp']

    suit_form_includes = [
        ('emails/previews/email_log_preview.html', 'top', ''),
    ]
