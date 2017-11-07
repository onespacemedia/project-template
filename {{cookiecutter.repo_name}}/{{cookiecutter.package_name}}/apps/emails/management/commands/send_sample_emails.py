from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ...models import EmailTemplate
from ...utils import send_email

data = {
    'user': get_user_model().objects.exclude(first_name=None).order_by('?')[0],
}


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('to_email')

    def handle(self, *args, **options):
        for template_obj in EmailTemplate.objects.all():
            self.stdout.write('[SENDING] {}\r'.format(template_obj.reference), ending='')
            self.stdout.flush()

            send_email(
                template_obj.reference,
                options['to_email'],
                **data
            )

            self.stdout.write('[ SENT ]  {}'.format(template_obj.reference))
