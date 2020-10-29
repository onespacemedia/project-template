import json

from cms.apps.media.models import MediaStorage
from django.db import models


class ThumbnailData(models.Model):
    key = models.CharField(
        max_length=256,
        primary_key=True,
        unique=True,
    )

    rendered = models.BooleanField(
        default=False,
    )

    options_json = models.TextField(
        blank=True,
    )

    media_file = models.FileField(
        upload_to='uploads/files',
        max_length=250,
        storage=MediaStorage(),
    )

    def set_options(self, options):
        self.options_json = json.dumps(options)

    def get_options(self):
        return json.loads(self.options_json)

    def __str__(self):
        return self.key

    class Meta:
        # Prevents integrity errors from race conditions
        select_on_save = True

    options = property(get_options, set_options)
