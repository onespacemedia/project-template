from os import execvp

from django.core.management import BaseCommand


class Command(BaseCommand):
    '''Shortcut for running Celery locally.'''
    def handle(self, *args, **options):
        celery_args = [
            'celery',
            '-A', '{{ cookiecutter.package_name }}',
            'worker',
            '-E',
            '--loglevel', 'info',
        ]
        print('>', *celery_args)
        execvp('celery', celery_args)
