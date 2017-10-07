import CommonMark
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import Context, Template
from django.template.loader import render_to_string

from .json import DjangoJSONEncoder


class EmailTemplate(models.Model):

    reference = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="This will be used in the application to send emails of this type. It's recommended that you don't change this value after it's defined. otherwise bad things may happen.",
    )

    # CharField as "Paul Smith <paul.smith@example.com>" is a valid value.
    from_email = models.CharField(
        max_length=300,
        default=settings.SERVER_EMAIL,
        help_text='Please ensure that the website is configured to send mail as this user.',
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
        help_text="""
            The main body of your email, rendered using <a href="http://commonmarkforhumans.com/" target="_blank">Commonmark</a>.  In general, the following merge tags are available to use:

            <ul>
                <li><strong>[fullname]</strong>: Mr Paul Smith</li>
                <li><strong>[firstname]</strong>: Paul</li>
                <li><strong>[lastname]</strong>: Smith</li>
                <li><strong>[email]</strong>: paul.smith@example.com</li>
            </ul>

            Other variables may be available depending on where the email template is being used.

            It's also possible to use full Jinja2 template formatting here, but check with the development team first.
        """
    )

    def get_html_version(self):
        from django.template import engines
        template = engines['backend'].from_string(self.content)

        # Pass the plain text template through the rendering engine so we're able to
        # use the full capabilities of Jinja.

        body = template.render(Context({}))

        # Generate the HTML version of the email and render it into the full template.
        body = CommonMark.commonmark(body).strip()

        return render_to_string('emails/base.html', {
            'body': body,
        })

    def __str__(self):
        return self.title

    class Meta:
        # Moves this model above logs in the sidebar
        verbose_name_plural = ' Email templates'


class EmailLog(models.Model):

    message_id = models.CharField(
        max_length=995,  # In theory..
    )

    email_template = models.ForeignKey(
        EmailTemplate,
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

    def get_html_version(self):
        return render_to_string('emails/base.html', self.kwargs)

    def to(self):
        return self.email_data['to']

    def from_email(self):
        return self.email_data['from_email']

    def subject(self):
        return self.email_data['subject']
