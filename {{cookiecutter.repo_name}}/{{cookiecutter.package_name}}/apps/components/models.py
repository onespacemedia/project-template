from django.db import models

from ...utils.models import HasLinkMixin


class CallToAction(HasLinkMixin, models.Model):

    kicker = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    title = models.CharField(
        max_length=140
    )

    def __str__(self):
        return self.title
