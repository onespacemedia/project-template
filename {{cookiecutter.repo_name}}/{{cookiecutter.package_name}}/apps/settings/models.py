from cms.apps.media.models import ImageRefField
from cms.models import HtmlField
from django.db import models
from django.template.defaultfilters import linebreaksbr
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe


class Setting(models.Model):

    name = models.CharField(
        max_length=1024,
        help_text='Name of the setting',
    )

    key = models.CharField(
        max_length=1024,
        help_text='The key used to reference the setting',
    )

    type = models.CharField(
        max_length=1024,
        choices=[
            ('string', 'String'),
            ('text', 'Text'),
            ('html', 'HTML'),
            ('number', 'Number'),
            ('image', 'Image'),
        ],
    )

    string = models.CharField(
        max_length=2048,
        blank=True,
        null=True,
    )

    text = models.TextField(
        blank=True,
        null=True,
    )

    html = HtmlField(
        'HTML',
        null=True,
        blank=True,
    )

    number = models.IntegerField(
        blank=True,
        null=True,
    )

    image = ImageRefField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @cached_property
    def value(self):
        return {
            'string': self.string,
            'text': linebreaksbr(mark_safe(self.text)),
            'html': mark_safe(self.html),
            'number': self.number,
            'image': self.image if self.image else '',
        }[self.type]
