from django.views.generic import CreateView, TemplateView

from ..emails.utils import send_email
from .forms import ContactForm
from .models import ContactSubmission


class ContactView(CreateView):
    model = ContactSubmission

    form_class = ContactForm

    template_name = 'contact/contact.html'

    def form_valid(self, form):
        context = {
            'reply_to': form.cleaned_data['email'],
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'phone_number': form.cleaned_data['phone_number'],
            'reason_for_enquiry': form.cleaned_data['reason_for_enquiry'],
            'email': form.cleaned_data['email'],
            'job_title': form.cleaned_data['job_title'],
            'message': form.cleaned_data['message'],
        }

        send_email('contact', **context)

        return super().form_valid(form)

    def get_success_url(self):
        return self.request.pages.current.reverse('contact_success')


class ContactSuccessView(TemplateView):
    template_name = 'contact/success.html'
