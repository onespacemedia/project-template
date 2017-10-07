from email.utils import make_msgid
from django.template import engines

import CommonMark
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
from django.template.loader import render_to_string

from .models import EmailLog, EmailTemplate


def send_email(reference, to, **kwargs):
    # We will allow Django's DoesNotExist exception to be raised here.
    template_obj = EmailTemplate.objects.get(reference=reference)
    msg_id = make_msgid(domain=settings.SITE_DOMAIN)

    email_data = {
        'from_email': template_obj.from_email,
        'bcc': [email for email in template_obj.bcc_list.split(',')],
        'subject': template_obj.subject,
        'headers': {
            'Message-ID': msg_id,
            'X-MC-PreserveRecipients': False,
        },
    }

    """
    The To value can be provided in a few different ways. The following are all valid:

    1. "john.smith@example.com"
    2. "John Smith <john.smith@example.com>"
    3. ["john.smith@example.com", "jane.smith@example.com"]
    4. ["John Smith <john.smith@example.com>", "Jane Smith <jane.smith@example.com>"]

    We detect the instance type and make changes where required.  Option 3 will be
    converted into the Option 4 format if `split_list` is not disabled.
    """

    if isinstance(to, str):
        to = [to]
    elif isinstance(to, (list, tuple)):
        if kwargs.get('split_list', True):
            to = [f'{email} <{email}>' for email in to]

    email_data['to'] = to

    """
    If a Reply-To value is defined, turn it into the format required.
    """

    if template_obj.reply_to:
        email_data['reply_to'] = [template_obj.reply_to]

    """
    Generate the email content.

    * Make substitutions for the pre-defined merge tags.
    * Render the plain text version by simply using the Markdown content.
    * Render the Markdown into HTML and inject that into our template.
    """

    # Add some additional data to the kwargs.
    if 'title' not in kwargs:
        kwargs['title'] = template_obj.title

    plain_text_template = template_obj.content

    # Replace the merge tags in the template.
    if 'user' in kwargs:
        plain_text_template = plain_text_template.replace('[fullname]', '{{ user.get_full_name() }}')
        plain_text_template = plain_text_template.replace('[firstname]', '{{ user.first_name }}')
        plain_text_template = plain_text_template.replace('[lastname]', '{{ user.last_name }}')
        plain_text_template = plain_text_template.replace('[email]', '{{ user.email }}')

    # Pass the plain text template through the rendering engine so we're able to
    # use the full capabilities of Jinja.

    template = engines['backend'].from_string(plain_text_template)
    email_data['body'] = template.render(Context(kwargs))

    # Generate the HTML version of the email and render it into the full template.
    kwargs['body'] = CommonMark.commonmark(email_data['body']).strip()
    html_template = render_to_string('emails/base.html', kwargs)

    # Allow testing that template rendering is error-free.
    if 'fake' in kwargs and kwargs['fake']:
        return

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
