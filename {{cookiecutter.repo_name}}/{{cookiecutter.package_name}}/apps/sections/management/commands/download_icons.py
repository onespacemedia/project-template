from __future__ import print_function

import os
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import SECTION_TYPES

IMAGE_ROOT = os.path.join(settings.SITE_ROOT, 'assets/img/sections/')
IMAGE_URL = 'https://github.com/onespacemedia/cms-icons/raw/master/png/i-_{}.png'


class Command(BaseCommand):
    help = 'Downloads the section icons.'

    def handle(self, *args, **options):
        try:
            os.makedirs(IMAGE_ROOT)
        except OSError:
            pass  # Directory already exists.

        icons = [
            section[1]['icon']
            for group in SECTION_TYPES
            for section in group[1]['sections']
            if 'icon' in section[1]
        ]

        for icon in icons:
            print(IMAGE_URL.format(icon))

            urllib.request.urlretrieve(
                IMAGE_URL.format(icon),
                os.path.join(IMAGE_ROOT, f'{icon}.png')
            )
