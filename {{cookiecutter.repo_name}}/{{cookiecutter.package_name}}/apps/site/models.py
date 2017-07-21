# from django.db import models

# class Footer(models.Model):
#
#     text = models.TextField(
#         blank=True,
#         null=True,
#     )
#
#     terms_of_use_link = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True,
#     )
#
#     legal_link = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True,
#     )
#
#     privacy_policy_link = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True,
#     )
#
#     def __str__(self):
#         return 'Footer'


# class FooterLink(models.Model):
#
#     footer = models.ForeignKey(
#         'site.Footer',
#     )
#
#     link_text = models.CharField(
#         max_length=100,
#     )
#
#     link_page = models.ForeignKey(
#         'pages.Page',
#         blank=True,
#         null=True,
#         help_text='If you want to link to an internal page, please use this.',
#         related_name='+'
#     )
#
#     link_url = models.CharField(
#         max_length=200,
#         blank=True,
#         null=True,
#         help_text='If you want to link to an external page, please use this.'
#     )
#
#     order = models.PositiveIntegerField()
#
#     class Meta:
#         ordering = ['order']
#
#     def __str__(self):
#         return self.link_text
#
#     def has_link(self):
#         return self.link_text and self.link_url or self.link_text and self.link_page
#
#     @property
#     def link_location(self):
#         return self.link_page.get_absolute_url() if self.link_page else self.link_url


# class Header(models.Model):
#
#     telephone_number = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True,
#     )
#
#     show_search = models.BooleanField(
#         default=True
#     )
#
#     def __str__(self):
#         return 'Header'


# class HeaderLink(models.Model):
#
#     header = models.ForeignKey(
#         'site.Header',
#     )
#
#     link_text = models.CharField(
#         max_length=100,
#     )
#
#     link_page = models.ForeignKey(
#         'pages.Page',
#         blank=True,
#         null=True,
#         help_text='If you want to link to an internal page, please use this.',
#         related_name='+'
#     )
#
#     link_url = models.CharField(
#         max_length=200,
#         blank=True,
#         null=True,
#         help_text='If you want to link to an external page, please use this.'
#     )
#
#     order = models.PositiveIntegerField()
#
#     class Meta:
#         ordering = ['order']
#
#     def __str__(self):
#         return self.link_text
#
#     def has_link(self):
#         return self.link_text and self.link_url or self.link_text and self.link_page
#
#     @property
#     def link_location(self):
#         return self.link_page.get_absolute_url() if self.link_page else self.link_url
