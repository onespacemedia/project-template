from cms import sitemaps
from cms.apps.media.models import ImageRefField
from cms.apps.pages.models import ContentBase, PageBase
from cms.models import HtmlField, SearchMetaBase
from django.db import models
from historylinks import shortcuts as historylinks


class Team(models.Model):

    title = models.CharField(
        max_length=255,
    )

    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.title


class People(ContentBase):

    classifier = 'apps'
    urlconf = '{{ project_name }}.apps.people.urls'

    per_page = models.PositiveIntegerField(
        'people per page',
        default=10,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.page.title


class Person(PageBase):

    page = models.ForeignKey(
        People
    )

    first_name = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    middle_name = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    last_name = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    job_title = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    team = models.ForeignKey(
        'Team',
        blank=True,
        null=True,
    )

    photo = ImageRefField(
        blank=True,
        null=True
    )

    bio = HtmlField(
        blank=True,
        null=True
    )

    email = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    linkedin_url = models.URLField(
        max_length=100,
        blank=True,
        null=True
    )

    twitter_username = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(
        default=0
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

    def get_twitter_url(self):
        twitter_username = self.twitter_username

        if twitter_username.startswith('http://') or twitter_username.startswith('https://'):
            return self.twitter_username

        if self.twitter_username.startswith('@'):
            twitter_username = twitter_username[1:]

        return f'https://twitter.com/{twitter_username}'

    def get_linkedin_url(self):
        linkedin_username = self.linkedin_username

        if linkedin_username.startswith('http://') or linkedin_username.startswith('https://'):
            return self.linked_username

        if linkedin_username.startswith('@'):
            linkedin_username = linkedin_username[1:]

        return f'https://www.linkedin.com/in/{linkedin_username}'

historylinks.register(Person)
sitemaps.register(Person)
