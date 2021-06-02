from cms.apps.media.models import ImageRefField
from cms.apps.pages.models import Page
from django.db import models
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

from ...utils.models import HasLinkMixin


class CallToAction(HasLinkMixin, models.Model):
    label = models.CharField(
        max_length=50,
        help_text="This is not shown on the front end of the site; it's to help you find it in the admin.",
    )

    title = models.CharField(
        max_length=255
    )

    image = ImageRefField(
        blank=True,
        null=True,
    )

    background_image = ImageRefField(
        blank=True,
        null=True,
        help_text="Will displayed behind the text content.",
    )

    def __str__(self):
        return self.title

    def render_card(self, page=None):
        return render_to_string('components/call_to_action.html', {
            'object': self,
            'page': page,
        })


class BaseSet(models.Model):
    label = models.CharField(
        max_length=50,
        help_text="This is not shown on the front end of the site; it's to help you find it in the admin.",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.label


class StatSet(BaseSet):
    pass


class LinkSet(BaseSet):
    pass


class CardSet(BaseSet):
    card_style = models.CharField(
        choices=[
            ('normal', 'Normal'),
            ('icon', 'Icon'),
        ],
        max_length=10,
        default='normal',
    )


class Statistic(models.Model):
    stat_set = models.ForeignKey(
        'components.StatSet',
        related_name='statistics',
        on_delete=models.CASCADE,
    )

    statistic = models.CharField(
        max_length=64,
    )

    text = models.TextField(
        max_length=200,
        blank=True,
        null=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.stat_set} - card {self.order}'

    def render_card(self):
        return render_to_string('components/statistics.html', {
            'object': self,
        })


class Link(HasLinkMixin):
    link_set = models.ForeignKey(
        'components.LinkSet',
        related_name='links',
        on_delete=models.CASCADE,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.link_set} - link {self.order}'


class Card(HasLinkMixin):
    card_set = models.ForeignKey(
        'components.CardSet',
        on_delete=models.CASCADE,
        related_name='cards',
    )

    title = models.CharField(
        max_length=100,
    )

    text = models.TextField(
        blank=True,
        null=True,
    )

    image = ImageRefField(
        blank=True,
        null=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    def __str__(self):
        return f'{self.card_set} - card {self.order}'

    def get_absolute_url(self):
        return self.link_location

    @cached_property
    def template(self):
        return f'components/cards/{self.card_set.card_style}.html'

    def render_card(self):
        return render_to_string(self.template, {
            'object': self,
        })


class Sidebox(HasLinkMixin, models.Model):
    label = models.CharField(
        max_length=50,
        help_text="This is not shown on the front end of the site; it's to help you find it in the admin.",
    )

    type = models.CharField(
        max_length=20,
        choices=[
            ('text', 'Text'),
        ]
    )

    title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    text = models.TextField(
        null=True,
        blank=True,
    )

    image = ImageRefField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['label']
        verbose_name_plural = 'sideboxes'

    def __str__(self):
        return self.label

    @cached_property
    def template(self):
        return f'components/sideboxes/{self.type}.html'

    def render_sidebox(self):
        return render_to_string(self.template, {
            'object': self,
        })
