from cms.apps.pages.models import Page
from django.db import models
from django.utils.functional import cached_property

from ...utils.models import HasLinkMixin


class Footer(models.Model):

    about_title = models.CharField(
        verbose_name='Title',
        max_length=50,
        blank=True,
        null=True,
    )

    about_text = models.TextField(
        max_length=400,
        verbose_name='Text',
        blank=True,
        null=True,
    )

    links_title = models.CharField(
        verbose_name='Footer links title',
        max_length=50,
        blank=True,
        null=True,
    )

    contact_title = models.CharField(
        verbose_name='Title',
        max_length=50,
        blank=True,
        null=True,
    )

    contact_address = models.TextField(
        max_length=200,
        blank=True,
        null=True,
    )

    contact_link_text = models.CharField(
        verbose_name='Link text',
        max_length=50,
        blank=True,
        null=True,
    )

    contact_link_page = models.ForeignKey(
        'pages.Page',
        on_delete=models.PROTECT,
        verbose_name='Link page',
        blank=True,
        null=True,
        related_name='+',
        help_text='Use this to link to an internal page.',
    )

    contact_link_url = models.CharField(
        verbose_name='Link URL',
        max_length=200,
        blank=True,
        null=True,
        help_text='Use this to link to an external page.',
    )

    terms_of_use_text = models.CharField(
        verbose_name='Terms of use text',
        max_length=255,
        blank=True,
        null=True,
        default='Terms of use',
    )

    terms_of_use_page = models.ForeignKey(
        'pages.Page',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='+',
        help_text='Use this to link to an internal page.',
    )

    terms_of_use_url = models.CharField(
        verbose_name='Terms of use URL',
        max_length=255,
        blank=True,
        null=True,
        help_text='Use this to link to an external page.',
    )

    legal_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default='Legal',
    )

    legal_page = models.ForeignKey(
        'pages.Page',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='+',
        help_text='Use this to link to an internal page.',
    )

    legal_url = models.CharField(
        verbose_name='Legal URL',
        max_length=255,
        blank=True,
        null=True,
        help_text='Use this to link to an external page.',
    )

    privacy_policy_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default='Privacy policy',
    )

    privacy_policy_page = models.ForeignKey(
        'pages.Page',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='+',
        help_text='Use this to link to an internal page.',
    )

    privacy_policy_url = models.CharField(
        verbose_name='Privacy policy URL',
        max_length=255,
        blank=True,
        null=True,
        help_text='Use this to link to an external page.',
    )

    def __str__(self):
        return 'Footer'

    @property
    def contact_has_link(self):
        return self.contact_link_location and self.contact_link_text

    @cached_property
    def contact_link_location(self):
        try:
            return self.contact_link_page.get_absolute_url() if self.contact_link_page else self.contact_link_url
        except (Page.DoesNotExist, AttributeError):
            return self.contact_link_url

    @cached_property
    def extra_links(self):
        return {
            'terms': {
                'label': self.terms_of_use_text,
                'has_link': self.terms_of_use_location and self.terms_of_use_text,
                'link_location': self.terms_of_use_location,
            },
            'legal': {
                'label': self.legal_text,
                'has_link': self.legal_location and self.legal_text,
                'link_location': self.legal_location,
            },
            'privacy': {
                'label': self.privacy_policy_text,
                'has_link': self.privacy_policy_location and self.privacy_policy_text,
                'link_location': self.privacy_policy_location,
            },
        }

    @cached_property
    def terms_of_use_location(self):
        try:
            return self.terms_of_use_page.get_absolute_url() if self.terms_of_use_page else self.terms_of_use_url
        except (Page.DoesNotExist, AttributeError):
            return self.terms_of_use_url

    @cached_property
    def legal_location(self):
        try:
            return self.legal_page.get_absolute_url() if self.legal_page else self.legal_url
        except (Page.DoesNotExist, AttributeError):
            return self.legal_url

    @cached_property
    def privacy_policy_location(self):
        try:
            return self.privacy_policy_page.get_absolute_url() if self.privacy_policy_page else self.privacy_policy_url
        except (Page.DoesNotExist, AttributeError):
            return self.privacy_policy_url

    @cached_property
    def columns(self):
        return {
            'about': self.about_title and self.about_text,
            'links': self.links_title and self.footerlink_set.count(),
            'contact': self.contact_title and self.contact_address,
        }


class FooterLink(HasLinkMixin, models.Model):

    footer = models.ForeignKey(
        'site.Footer',
        on_delete=models.PROTECT,
    )

    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.link_text


class Header(models.Model):

    show_search = models.BooleanField(
        default=True
    )

    def __str__(self):
        return 'Header'


class HeaderLink(HasLinkMixin, models.Model):

    header = models.ForeignKey(
        'site.Header',
        on_delete=models.PROTECT,
    )

    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.link_text
