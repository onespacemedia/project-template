from cms import sitemaps
from cms.apps.pages.models import ContentBase
from cms.models import HtmlField, PageBase
from django.db import models
from historylinks import shortcuts as historylinks


class Careers(ContentBase):

    classifier = 'apps'
    urlconf = '{{ project_name }}.apps.careers.urls'

    per_page = models.PositiveIntegerField(
        'careers per page',
        default=10,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.page.title


class Career(PageBase):

    page = models.ForeignKey(
        Careers
    )

    location = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    summary = models.TextField(
        blank=True,
        null=True
    )

    description = HtmlField()

    email_address = models.EmailField()

    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.page.page.reverse('career_detail', kwargs={
            'slug': self.slug,
        })

historylinks.register(Career)
sitemaps.register(Career)
