from email.utils import make_msgid

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from html2text import html2text

from .models import EmailLog, EmailTemplate


def send_email(reference, to=None, **kwargs):  # pylint: disable=too-complex
    template_obj = EmailTemplate.objects.filter(reference=reference).first()

    # As long as developers set up email templates properly;
    # it should be impossible to cause an error by using this app.
    # We can create an empty template object if one doesn't exist
    if not template_obj:
        template_obj = EmailTemplate.objects.create(
            reference=reference,
        )

    kwargs['object'] = template_obj
    kwargs['settings'] = settings

    # Does this email template have a `to_email` defined?
    if template_obj.to_email:
        to = [email for email in template_obj.to_email.split(',')]
    elif not to:
        raise ValueError("You must supply the `to` value if the email template doesn't.")

    msg_id = make_msgid(domain=settings.SITE_DOMAIN)

    email_data = {
        'from_email': settings.DEFAULT_FROM_EMAIL,
        'bcc': [email for email in template_obj.bcc_list.split(',')] if template_obj.bcc_list else [],
        'subject': template_obj.subject,
        'headers': {
            'Message-ID': msg_id,
            'X-MC-PreserveRecipients': False,
        },
    }

    # The To value can be provided in a few different ways. The following are all valid:
    #
    # 1. "john.smith@example.com"
    # 2. "John Smith <john.smith@example.com>"
    # 3. ["john.smith@example.com", "jane.smith@example.com"]
    # 4. ["John Smith <john.smith@example.com>", "Jane Smith <jane.smith@example.com>"]
    #
    # We detect the instance type and make changes where required.  Option 3 will be
    # converted into the Option 4 format if `split_list` is not disabled.

    if isinstance(to, str):
        to = [to]
    elif isinstance(to, (list, tuple)):
        if kwargs.get('split_list', True):
            to = [f'{email} <{email}>' for email in to]

    email_data['to'] = to

    # If a Reply-To value is defined, turn it into the format required.
    email_data['reply_to'] = [kwargs.get('reply_to') or template_obj.reply_to or '']

    # Generate the email content.
    #
    # * Make substitutions for the pre-defined merge tags.
    # * Render the plain text version by simply using the Markdown content.
    # * Render the Markdown into HTML and inject that into our template.

    # Add some additional data to the kwargs.
    if 'title' not in kwargs:
        kwargs['title'] = template_obj.title

    html_template = render_to_string(f'emails/{template_obj.reference}.html', kwargs)
    # Create a text version of the email template
    email_data['body'] = html2text(html_template)

    # Allow testing that template rendering is error-free.
    if 'fake' in kwargs and kwargs['fake']:
        return

    kwargs.pop('object')
    kwargs.pop('settings')

    # Store this email in the database.
    EmailLog.objects.create(
        message_id=msg_id,
        email_template=template_obj,
        email_data=email_data,
        kwargs=kwargs,
    )

    # Build up the email object.
    email_obj = EmailMultiAlternatives(**email_data)
    email_obj.attach_alternative(html_template, 'text/html')

    # Attach any additional information.
    if kwargs.get('ics'):
        email_obj.attach('event.ics', kwargs['ics'], 'text/calendar')

    # Finally, send the email.
    email_obj.send(fail_silently=kwargs.get('fail_silently', False))
