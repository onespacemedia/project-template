from cms.apps.pages.models import Page
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property


class CallToAction(models.Model):

    kicker = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    title = models.CharField(
        max_length=140
    )

    link_text = models.CharField(
        max_length=100,
    )

    link_page = models.ForeignKey(
        Page,
        blank=True,
        null=True,
        help_text='If you want to link to an internal page, please use this.',
    )

    link_url = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='If you want to link to an external page, please use this.',
    )

    def __str__(self):
        return self.title

    def clean(self):
        if not self.link_page and not self.link_url:
            raise ValidationError({
                'link_page': 'Please supply 1 of "link page" or "link URL"',
            })

    @property
    def has_link(self):
        return self.link_location and self.link_text

    @cached_property
    def link_location(self):
        try:
            return self.link_page.get_absolute_url() if self.link_page else self.link_url
        except (Page.DoesNotExist, AttributeError):
            return self.link_url
