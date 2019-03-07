from cms import sitemaps
from cms.apps.pages.models import ContentBase
from cms.models import HtmlField, PageBase
from django.db import models
from historylinks import shortcuts as historylinks


class Faqs(ContentBase):

    classifier = 'apps'
    icon = 'cms-icons/faqs.png'
    urlconf = '{{ cookiecutter.package_name }}.apps.faqs.urls'

    per_page = models.PositiveIntegerField(
        'FAQs per page',
        default=10,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'FAQs'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.page.title


class Category(models.Model):

    title = models.CharField(
        max_length=255,
    )

    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'categories'


class Faq(PageBase):

    page = models.ForeignKey(
        Faqs,
        on_delete=models.PROTECT,
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    question = models.CharField(
        max_length=256
    )

    answer = HtmlField()

    order = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.question

    class Meta:
        unique_together = [['page', 'slug']]
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['order', 'question']

    def get_absolute_url(self):
        return self.page.page.reverse('faq_detail', kwargs={
            'slug': self.slug,
        })

historylinks.register(Faq)
sitemaps.register(Faq)
