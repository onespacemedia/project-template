import json

from cms.apps.media.models import MediaStorage
from django.db import models


class ThumbnailData(models.Model):
    key = models.CharField(
        max_length=250,
        primary_key=True,
        unique=True,
    )

    rendered = models.BooleanField(
        default=False,
    )

    options_json = models.TextField(
        blank=True,
    )

    media_file = models.CharField(
        max_length=512,
    )

    @classmethod
    def create(cls, key, file_, options, rendered=False):
        return cls(key=key, media_file=file_.name, options_json=json.dumps(options), rendered=rendered)

    def set_options(self, options):
        self.options_json = json.dumps(options)

    def get_options(self):
        return json.loads(self.options_json)

    options = property(get_options, set_options)

    def get_file(self):
        return MediaStorage().open(self.media_file)

    def set_file(self, file_):
        self.media_file = file_.name

    file = property(get_file, set_file)

    def __str__(self):
        return self.key

    class Meta:
        # Prevents integrity errors from race conditions
        select_on_save = True
