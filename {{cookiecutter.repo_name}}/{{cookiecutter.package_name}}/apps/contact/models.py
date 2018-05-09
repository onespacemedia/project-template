from cms.apps.pages.models import ContentBase
from cms.models import HtmlField
from django.db import models


class Contact(ContentBase):

    # The urlconf used to power this content's views.
    urlconf = '{{cookiecutter.package_name}}.apps.contact.urls'

    call_to_action = models.ForeignKey(
        'components.CallToAction',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    hero_kicker = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='If this is left blank it will use the page title',
    )

    hero_title = models.CharField(
        max_length=255,
    )

    form_email_address = models.CharField(
        max_length=255,
        help_text='This is the email address form submissions will be sent to.',
    )

    form_title = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    success_page_title = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    success_page_content = HtmlField(
        blank=True,
        null=True,
    )

    fieldsets = [
        [None, {
            'fields': ['call_to_action'],
        }],
        ['Hero', {
            'fields': ['hero_kicker', 'hero_title'],
        }],
        ['Form', {
            'fields': ['form_email_address', 'form_title'],
        }],
        ['Success page', {
            'fields': ['success_page_title', 'success_page_content'],
        }],
    ]

    def __str__(self):
        return self.page.title


class ContactSubmission(models.Model):

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    job_title = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    reason_for_enquiry = models.CharField(
        max_length=100,
    )

    message = models.TextField(
        'Your message',
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Contact submission from {self.first_name} {self.last_name}'
