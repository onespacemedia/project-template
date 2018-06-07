from cms.apps.pages.models import ContentBase
from cms.models import HtmlField
from django.db import models


class Contact(ContentBase):

    # The urlconf used to power this content's views.
    urlconf = '{{cookiecutter.package_name}}.apps.contact.urls'

    icon = 'cms-icons/form.png'

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
        help_text='If this is left blank it will use the page title.',
        verbose_name='Kicker',
    )

    hero_title = models.CharField(
        max_length=255,
        verbose_name='Title',
    )

    form_email_address = models.CharField(
        max_length=255,
        help_text='Form submissions will be sent to these addresses. Separate multiple emails with a comma or space',
        verbose_name='Email Address',
    )

    form_title = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Title',
    )

    success_page_title = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Title',
    )

    success_page_content = HtmlField(
        blank=True,
        null=True,
        verbose_name='Content',
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

    @property
    def get_email_addresses(self):
        # Strip out commas if comma separated.
        emails = self.form_email_address.replace(',', ' ')

        emails = emails.split(' ')
        for email in emails:
            email.strip()

        # Filter out empty strings
        emails = list(filter(lambda a: a != '', emails))

        return emails


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
