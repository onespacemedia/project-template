from cms import sitemaps
from cms.apps.media.models import ImageRefField
from cms.models import PageBase
from django.db import models
from historylinks import shortcuts as historylinks


class Partner(PageBase):

    summary = models.TextField(
        max_length=140,
        blank=True,
        null=True
    )

    logo = ImageRefField()

    website = models.CharField(
        max_length=140,
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

historylinks.register(Partner)
sitemaps.register(Partner)
