from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from ...utils.utils import url_from_path


class ProjectPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'frm-Form_Input'
        self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label

    def send_mail(self, subject_template_name, email_template_name,   # pylint: disable=too-many-arguments
                  context, from_email, to_email, html_email_template_name=None):

        reset_url = reverse('password_reset_confirm', kwargs={
            'uidb64': context['uid'],
            'token': context['token'],
        })
        context['reset_url'] = url_from_path(reset_url)
        context['settings'] = settings

        email_text_template = render_to_string('emails/password-reset.txt', context)
        email_html_template = render_to_string('emails/password-reset.html', context)

        email = EmailMultiAlternatives(
            subject=f'Your password reset on {settings.SITE_NAME}',
            body=email_text_template,
            reply_to=[settings.DEFAULT_FROM_EMAIL],
            to=[to_email],
        )

        email.attach_alternative(email_html_template, 'text/html')

        try:
            email.send()
        except:  # pylint:disable=bare-except
            if settings.DEBUG:
                raise


class ProjectSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].help_text = "Your password must be at least 8 characters long and cannot be entirely numeric"
        self.fields['new_password2'].help_text = "Enter the same password for verification."

        self.fields['new_password1'].widget.attrs['class'] = 'frm-Form_Input'
        self.fields['new_password1'].widget.attrs['placeholder'] = self.fields['new_password1'].label

        self.fields['new_password2'].widget.attrs['class'] = 'frm-Form_Input'
        self.fields['new_password2'].widget.attrs['placeholder'] = self.fields['new_password2'].label
