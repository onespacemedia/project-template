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


class StatSet(models.Model):
    label = models.CharField(
        max_length=50,
        help_text="This is not shown on the front end of the site; it's to help you find it in the admin.",
    )

    def __str__(self):
        return self.label


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


class LinkSet(models.Model):
    label = models.CharField(
        max_length=50,
        help_text="This is not shown on the front end of the site; it's to help you find it in the admin.",
    )

    def __str__(self):
        return self.label


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
