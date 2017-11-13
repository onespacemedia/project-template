from cms.apps.pages.models import Page
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property


class Footer(models.Model):

    text = models.TextField(
        blank=True,
        null=True,
    )

    terms_of_use_page = models.ForeignKey(
        'pages.Page',
        blank=True,
        null=True,
    )

    terms_of_use_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    legal_page = models.ForeignKey(
        'pages.Page',
        blank=True,
        null=True,
    )

    legal_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    privacy_policy_page = models.ForeignKey(
        'pages.Page',
        blank=True,
        null=True,
    )

    privacy_policy_link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self):
        return 'Footer'

    @cached_property
    def terms_of_use_link_location(self):
        if self.terms_of_use_page_id:
            try:
                return self.terms_of_use_page.get_absolute_url()
            except Page.DoesNotExist:
                pass
        return self.terms_of_use_link

    @cached_property
    def legal_link_location(self):
        if self.legal_page_id:
            try:
                return self.legal_page.get_absolute_url()
            except Page.DoesNotExist:
                pass
        return self.legal_link

    @cached_property
    def privacy_policy_link_location(self):
        if self.privacy_policy_page_id:
            try:
                return self.privacy_policy_page.get_absolute_url()
            except Page.DoesNotExist:
                pass
        return self.privacy_policy_link


class FooterLink(models.Model):

    footer = models.ForeignKey(
        'site.Footer',
    )

    link_text = models.CharField(
        max_length=100,
    )

    link_page = models.ForeignKey(
        'pages.Page',
        blank=True,
        null=True,
        help_text='If you want to link to an internal page, please use this.',
        related_name='+'
    )

    link_url = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='If you want to link to an external page, please use this.'
    )

    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.link_text

    def clean(self):
        if self.link_page or self.link_url:
            pass
        else:
            raise ValidationError({
                'link_page': 'Please supply either a link page or a link url.'
            })

    def has_link(self):
        return self.link_location and self.link_text

    @cached_property
    def link_location(self):
        if self.link_page_id:
            try:
                return self.link_page.get_absolute_url()
            except Page.DoesNotExist:
                pass
        return self.link_url


class Header(models.Model):

    show_search = models.BooleanField(
        default=True
    )

    def __str__(self):
        return 'Header'


class HeaderLink(models.Model):

    header = models.ForeignKey(
        'site.Header',
    )

    link_text = models.CharField(
        max_length=100,
    )

    link_page = models.ForeignKey(
        'pages.Page',
        blank=True,
        null=True,
        help_text='If you want to link to an internal page, please use this.',
        related_name='+'
    )

    link_url = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='If you want to link to an external page, please use this.'
    )

    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.link_text

    def clean(self):
        if self.link_page or self.link_url:
            pass
        else:
            raise ValidationError({
                'link_page': 'Please supply either a link page or a link url.'
            })

    def has_link(self):
        return self.link_location and self.link_text

    @cached_property
    def link_location(self):
        if self.link_page_id:
            try:
                return self.link_page.get_absolute_url()
            except Page.DoesNotExist:
                pass
        return self.link_url
