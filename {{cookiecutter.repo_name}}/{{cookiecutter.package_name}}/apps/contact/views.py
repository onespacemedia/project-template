from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.generic import CreateView, TemplateView

from ..contact.models import ContactSubmission
from .forms import ContactForm


class ContactView(CreateView):
    model = ContactSubmission

    form_class = ContactForm

    template_name = 'contact/contact.html'

    def form_valid(self, form):
        context = {
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'phone_number': form.cleaned_data['phone_number'],
            'reason_for_enquiry': form.cleaned_data['reason_for_enquiry'],
            'email': form.cleaned_data['email'],
            'job_title': form.cleaned_data['job_title'],
            'message': form.cleaned_data['message'],
            'settings': settings,
        }

        email_text_template = render_to_string('emails/contact-form.txt', context)

        email_html_template = render_to_string('emails/contact-form.html', context)

        email = EmailMultiAlternatives(
            subject=f'New contact form submission on {settings.SITE_NAME}',
            body=email_text_template,
            reply_to=[form.cleaned_data['email']],
            to=[self.request.pages.current.content.form_email_address],
        )

        email.attach_alternative(email_html_template, 'text/html')


        try:
            email.send()
        except:  # pylint:disable=bare-except
            if settings.DEBUG:
                raise

        return super().form_valid(form)

    def get_success_url(self):
        return self.request.pages.current.reverse('contact_success')


class ContactSuccessView(TemplateView):
    template_name = 'contact/success.html'
