import re

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import \
    PasswordResetForm as BasePasswordResetForm
from django.contrib.auth.forms import SetPasswordForm as BaseSetPasswordForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from ...utils.utils import url_from_path


class PasswordResetForm(BasePasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'frm-Form_Input'
        self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = get_user_model()._default_manager.filter(
            email__iexact=email,
            is_active=True,
        )

        return [u for u in active_users]

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            # pylint:disable=unused-variable
            self.get_users(email)[0]
        except IndexError:
            raise forms.ValidationError(
                u'This email address does not seem to be associated with a {} account.'.format(
                    settings.SITE_NAME
                )
            )
        return email

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


class SetPasswordForm(BaseSetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].help_text = "Your password must be at least 8 characters long and contain at least 1 uppercase character, 1 lowercase character and at least 1 number."
        self.fields['new_password2'].help_text = "Enter the same password for verification."

        self.fields['new_password1'].widget.attrs['class'] = 'frm-Form_Input'
        self.fields['new_password1'].widget.attrs['placeholder'] = self.fields['new_password1'].label

        self.fields['new_password2'].widget.attrs['class'] = 'frm-Form_Input'
        self.fields['new_password2'].widget.attrs['placeholder'] = self.fields['new_password2'].label
