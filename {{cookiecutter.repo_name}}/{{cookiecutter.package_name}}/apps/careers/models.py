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


class CareerLocation(models.Model):

    title = models.CharField(
        max_length=100,
    )

    street_address = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )

    city = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )

    region = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )

    postcode = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )

    country = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        help_text="The country's ISO ALPHA-2 code"
    )

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title


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

    location = models.ForeignKey(
        CareerLocation,
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

    date_posted = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    # Schema Fields
    employment_type = models.CharField(
        choices=[
            ('FULL_TIME', 'Full time'),
            ('PART_TIME', 'Part time'),
            ('CONTRACTOR', 'Contract'),
            ('TEMPORARY', 'Temporary'),
            ('INTERN', 'Internship'),
        ],
        max_length=16,
        blank=True,
        null=True,
    )

    education_requirements = models.CharField(
        max_length=512,
        blank=True,
        null=True,
    )

    experience_requirements = models.CharField(
        max_length=512,
        blank=True,
        null=True,
    )

    qualifications = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text='Specific qualifications required for this role.'
    )

    responsibilities = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text='Responsibilities associated with this role.'
    )

    skills = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text='Skills required to fulfill this role.'
    )

    work_hours = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text='The typical working hours for this job (e.g. 1st shift, night shift, 8am-5pm).'
    )

    estimated_salary = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    base_salary = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ['order']

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
