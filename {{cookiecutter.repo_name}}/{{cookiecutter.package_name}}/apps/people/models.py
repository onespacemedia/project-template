from cms import sitemaps
from cms.apps.media.models import ImageRefField
from cms.apps.pages.models import ContentBase
from cms.models import HtmlField, SearchMetaBase
from django.db import models
from django.utils.functional import cached_property
from historylinks import shortcuts as historylinks


class Team(models.Model):

    title = models.CharField(
        max_length=255,
    )

    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.title


class People(ContentBase):

    classifier = 'apps'
    icon = 'cms-icons/people.png'
    urlconf = '{{ cookiecutter.package_name }}.apps.people.urls'

    per_page = models.PositiveIntegerField(
        'people per page',
        default=10,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.page.title


class Person(SearchMetaBase):

    page = models.ForeignKey(
        People,
        on_delete=models.PROTECT,
    )

    slug = models.SlugField(
        unique=True,
    )

    title = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text='This is their formal title, not their job title.',
    )

    first_name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    middle_name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    job_title = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    team = models.ForeignKey(
        'Team',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    photo = ImageRefField(
        blank=True,
        null=True,
    )

    bio = HtmlField(
        blank=True,
        null=True,
    )

    email = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    linkedin = models.CharField(
        'LinkedIn',
        max_length=100,
        blank=True,
        null=True,
        help_text="This can either be a username (e.g. @person) or a full URL; it'll be normalised to a URL on save.",
    )

    twitter = models.CharField(
        'Twitter',
        max_length=100,
        blank=True,
        null=True,
        help_text="This can either be a username (e.g. @person) or a full URL; it'll be normalised to a username on save.",
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'people'

    def __str__(self):
        fields = ['title', 'first_name', 'middle_name', 'last_name']
        parts = [getattr(self, field) for field in fields if getattr(self, field)]

        return ' '.join(parts)

    def get_absolute_url(self):
        return self.page.page.reverse('person_detail', kwargs={
            'slug': self.slug,
        })

    @cached_property
    def twitter_url(self):
        if self.twitter:
            return f'https://twitter.com/{self.twitter}'

    @property
    def colleagues(self):
        return self.team.person_set.exclude(pk=self.pk)

historylinks.register(Person)
sitemaps.register(Person)
