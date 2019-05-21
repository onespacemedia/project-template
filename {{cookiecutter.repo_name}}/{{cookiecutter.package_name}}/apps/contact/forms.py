from captcha.fields import ReCaptchaField
from django import forms

from .models import ContactSubmission


class ContactForm(forms.ModelForm):

    captcha = ReCaptchaField()

    class Meta:
        model = ContactSubmission
        fields = '__all__'
