import csv
from io import StringIO

from cms.apps.pages.admin import page_admin
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from django.utils.timezone import now
from reversion.admin import VersionAdmin

from ..sections.admin import ContentSectionInline
from .models import Contact, ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(VersionAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'job_title', 'reason_for_enquiry', 'created']

    # Rewrite to use django_import_export?
    def export_view(self, request):
        '''Exports all contact form submissions to a CSV.'''
        fd = StringIO()
        csv_writer = csv.writer(fd)
        csv_writer.writerow(['Name', 'Reason', 'Email', 'Phone', 'Job_Title', 'Message', 'Date'])

        for submission in ContactSubmission.objects.all():
            csv_writer.writerow([
                submission,
                submission.reason_for_enquiry,
                submission.email,
                submission.phone_number,
                submission.job_title,
                submission.message,
                submission.created,
            ])
        fd.seek(0)

        response = HttpResponse(fd.read())
        response['Content-Type'] = 'text/csv'
        response['Content-Disposition'] = (
            'attachment;filename="components-bureau-submissions-{}.csv'.format(
                now().isoformat()
            )
        )
        return response

    def get_urls(self):
        patterns = super().get_urls()
        patterns = [
            url(r'^export/$', self.export_view, name='submission_export'),
        ] + patterns
        return patterns


page_admin.register_content_inline(Contact, ContentSectionInline)
