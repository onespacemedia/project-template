# from cms.apps.pages.models import Page
# from django.db import models


# class CallToAction(models.Model):

#     super_title = models.CharField(
#         max_length=100,
#         blank=True,
#         null=True
#     )

#     title = models.CharField(
#         max_length=140
#     )

#     link_page = models.ForeignKey(
#         Page,
#         blank=True,
#         null=True,
#         help_text='If you want to link to an internal page, please use this.'
#     )

#     link_url = models.CharField(
#         max_length=200,
#         blank=True,
#         null=True,
#         help_text='If you want to link to an external page, please use this.'
#     )

#     def __unicode__(self):
#         return self.title

#     @property
#     def link_location(self):
#         return self.link_page.get_absolute_url() if self.link_page else self.link_url
