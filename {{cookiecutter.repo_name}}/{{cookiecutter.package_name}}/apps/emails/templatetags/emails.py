from django import template

from ..models import EmailLog, EmailTemplate

register = template.Library()


@register.simple_tag
def get_email_log_html(object_id):
    return EmailLog.objects.get(pk=object_id).get_html_version()


@register.simple_tag
def get_email_template_html(object_id):
    return EmailTemplate.objects.get(pk=object_id).get_html_version()
