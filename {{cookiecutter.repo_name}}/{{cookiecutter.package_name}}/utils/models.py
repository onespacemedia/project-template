from cms.apps.pages.models import Page
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property

from .video import get_video_info


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
        related_name='+',
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


class VideoMixin(models.Model):
    video = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Please provide a youtube.com or vimeo.com URL',
    )

    # Secret fields - populated from the URL when the form is saved.
    video_iframe_url = models.TextField(
        null=True,
        blank=True,
    )

    video_id = models.CharField(
        max_length=32,
        blank=True,
        null=True,
    )

    video_service = models.CharField(
        max_length=32,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def clean(self):
        if self.video:
            info = get_video_info(self.video)
            if info:
                self.video_iframe_url = info['src']
                if not self.video_iframe_url:
                    raise ValidationError({
                        'video': "Couldn't determine how to embed this video. Maybe the video's privacy settings disallow embedding?"
                    })
                self.video_id = info['id']
                self.video_service = info['service']
        else:
            self.video_iframe_url = ''
            self.video_id = ''
            self.video_service = ''
