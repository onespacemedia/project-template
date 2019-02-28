from cms import sitemaps
from cms.apps.pages.models import ContentBase
from cms.models import HtmlField, PageBase, PageBaseManager
from django.db import models
from django.db.models import Q
from django.utils.timezone import now
from historylinks import shortcuts as historylinks


class Careers(ContentBase):

    classifier = 'apps'
    icon = 'cms-icons/careers.png'
    urlconf = '{{ cookiecutter.package_name }}.apps.careers.urls'

    per_page = models.PositiveIntegerField(
        'careers per page',
        default=10,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.page.title


class CareerQuerySet(models.QuerySet):
    def select_open(self):
        return self.filter(
            Q(closing_date=None) |
            Q(closing_date__gte=now().date()),
        )

    def select_closed(self):
        return self.exclude(closing_date=None).filter(
            closing_date__lt=now().date(),
        )


class Career(PageBase):
    objects = PageBaseManager.from_queryset(CareerQuerySet)()

    page = models.ForeignKey(
        Careers,
        on_delete=models.PROTECT,
    )

    closing_date = models.DateField(
        null=True,
        blank=True,
        help_text='The date after which this career should no longer be listed on the site. If you leave this empty, it will never be de-listed.',
    )

    location = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )

    summary = models.TextField(
        blank=True,
        null=True,
    )

    description = HtmlField()

    email_address = models.EmailField(
        null=True,
        blank=True,
        help_text='An email address to which applications should be sent.',
    )

    application_url = models.URLField(
        'application URL',
        null=True,
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ['order']
        unique_together = [['page', 'slug']]

    def __str__(self):
        return self.title

    def is_open(self):
        return self.closing_date is None or self.closing_date >= now().date()

    def get_absolute_url(self):
        return self.page.page.reverse('career_detail', kwargs={
            'slug': self.slug,
        })

historylinks.register(Career)
sitemaps.register(Career)
