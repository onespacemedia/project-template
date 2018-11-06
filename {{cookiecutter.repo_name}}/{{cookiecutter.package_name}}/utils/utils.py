'''Miscellaneous helpful functions.'''

from cms.apps.media.templatetags.media import thumbnail
from django.conf import settings


def get_related_items(candidate_querysets, count=3, exclude=None):
    '''
    Returns `count` related items for an object given one or more candidate
    querysets. `exclude` should be an object you would like to exclude; for
    example, if you are trying to get similar news articles for a certain
    article, you will want to pass the article in question as the `exclude`
    parameter.

    An example from the news app:

    def get_related_articles(self, count=3):
        candidate_querysets = [
            Article.objects.filter(categories__in=self.categories.all()),
            Article.objects.all(),
        ]
        return get_related_items(candidate_querysets, count=count, exclude=self)
    '''
    objects = []

    for candidate_queryset in candidate_querysets:
        if exclude:
            candidate_queryset = candidate_queryset.exclude(pk=exclude.pk)

        objects += list(
            candidate_queryset.exclude(
                pk__in=[obj_existing.pk for obj_existing in objects]
            ).distinct()[:count - len(objects)]
        )

        if len(objects) >= count:
            break

    return objects


def url_from_path(path, request=None):
    if path.startswith('http://') or path.startswith('https://'):
        return path

    if not path.startswith('/'):
        path = '/' + path

    if request and not request.is_secure():
        secure_part = ''
    else:
        secure_part = 's'

    return 'http{}://{}{}'.format(secure_part, settings.SITE_DOMAIN, path)


ORGANISATION_SCHEMA = {
    '@type': 'Organization',
    'name': settings.SITE_NAME,
    'email': settings.SERVER_EMAIL,
    'sameAs': 'https://www.{}'.format(settings.SITE_DOMAIN),
    'logo': {
        '@context': 'http://schema.org',
        '@type': 'ImageObject',
        'name': '{} logo'.format(settings.SITE_NAME),
        'url': 'https://www.{}/static/img/logo.png'.format(settings.SITE_DOMAIN),
        'description': 'Logo for {}'.format(settings.SITE_NAME),
        'copyrightHolder': '{}'.format(settings.SITE_NAME)
    }
}


def schema_image(image):
    img = thumbnail(image.file, '1500')
    return {
        '@context': 'http://schema.org',
        '@type': 'ImageObject',
        'name': image.title,
        'url': 'https://www.{}{}'.format(settings.SITE_DOMAIN, img.url),
        'height': img.height,
        'width': img.width,
        'description': image.alt_text if image.alt_text else '',
        'author': image.attribution if image.attribution else '',
        'copyrightHolder': image.copyright if image.copyright else ''
    }
