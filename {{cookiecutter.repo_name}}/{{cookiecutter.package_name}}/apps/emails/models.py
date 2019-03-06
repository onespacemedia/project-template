from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models

from .json import DjangoJSONEncoder


class EmailTemplate(models.Model):

    reference = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        unique=True,
        help_text="This will be used in the application to send emails of this type. It's recommended that you don't change this value after it's defined. otherwise bad things may happen.",
    )

    # CharField as "Paul Smith <paul.smith@example.com>" is a valid value.
    to_email = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text='For automated emails, such as contact forms, you can define where the emails are send.',
    )

    # CharField as "Paul Smith <paul.smith@example.com>" is a valid value.
    reply_to = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text='If you would like recipients to reply to a different address, enter that here.',
    )

    bcc_list = models.CharField(
        "BCC list",
        max_length=300,
        null=True,
        blank=True,
        default=settings.SERVER_EMAIL,
        help_text='Additional email addresses that should recieve a copy of this email (comma separated).',
    )

    subject = models.CharField(
        max_length=300,
        default='{}: '.format(settings.SITE_NAME),
        help_text="The text shown in the recipient's email client.",
    )

    title = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text='Displayed at the top of the email, just before the content.',
    )

    content = models.TextField(
        help_text='The main body of your email, rendered using <a href="http://commonmarkforhumans.com/" target="_blank">Commonmark</a>.'
    )

    def __str__(self):
        return self.title or self.subject

    def get_html_version(self):
        # TODO
        return ''

    class Meta:
        # Moves this model above logs in the sidebar
        verbose_name_plural = 'email templates'


class EmailLog(models.Model):

    message_id = models.CharField(
        max_length=995,  # In theory..
    )

    email_template = models.ForeignKey(
        EmailTemplate,
        on_delete=models.SET_NULL,
    )

    email_data = JSONField(
        encoder=DjangoJSONEncoder,
    )

    kwargs = JSONField(
        encoder=DjangoJSONEncoder,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.message_id

    def to(self):
        return self.email_data.get('to')

    def from_email(self):
        return self.email_data.get('from_email')

    def subject(self):
        return self.email_data.get('subject')

    def get_html_version(self):
        # TODO
        return ''
