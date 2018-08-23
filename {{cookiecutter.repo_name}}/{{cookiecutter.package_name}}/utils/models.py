from cms.apps.pages.models import Page
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property


class HasLinkMixin(models.Model):

    link_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    link_page = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='Use this to link to an internal page.',
    )

    link_url = models.CharField(
        'link URL',
        max_length=200,
        blank=True,
        null=True,
        help_text='Use this to link to an external page.',
    )

    class Meta:
        abstract = True

    def clean(self):
        if self.link_text and (not self.link_page and not self.link_url):
            raise ValidationError({
                'link_page': 'Please supply either a "link page" or "link URL"',
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
