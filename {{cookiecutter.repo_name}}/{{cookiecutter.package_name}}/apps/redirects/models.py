import re

from django.db import models
from django.utils.safestring import mark_safe


class Redirect(models.Model):

    type = models.CharField(
        max_length=3,
        choices=[
            ('301', 'Permanent'),
            ('302', 'Temporary'),
        ],
        default='301',
    )

    old_path = models.CharField(
        'redirect from',
        max_length=200,
        db_index=True,
        unique=True,
        help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'."
    )

    new_path = models.CharField(
        'redirect to',
        max_length=200,
        blank=True,
        help_text="This can be either an absolute path (as above) or a full URL starting with 'http://'."
    )

    regular_expression = models.BooleanField(
        default=False,
        help_text=mark_safe(
            "This will allow using regular expressions to match and "
            "replace patterns in URLs. See the "
            "<a href='https://docs.python.org/2/library/re.html' target='_blank'>Python "
            "regular expression documentation</a> for details."
        )
    )

    test_path = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text=(
            "You will need to specify a test path to ensure your regular "
            "expression is valid."
        ),
    )

    class Meta:
        verbose_name = 'redirect'
        verbose_name_plural = 'redirects'
        ordering = ('old_path',)

    def __str__(self):
        return self.old_path

    def sub_path(self, path):
        """ If this redirect is a regular expression, it will return a
        rewritten version of `path`; otherwise returns the `new_path`. """
        if not self.regular_expression:
            return self.new_path
        return re.sub(self.old_path, self.new_path, path)

    def clean(self):
        path = self.new_path

        if path.startswith('http'):
            path = path.split(settings.SITE_DOMAIN)[-1]

        if path.endswith('/'):
            path_options = [path[:-1], path]
        else:
            path_options = [path, f'{path}/']

        for redirect in Redirect.objects.all():
            if redirect.old_path in path_options:
                raise ValidationError({
                    'new_path': 'There is already a redirect from this URL. Please do not redirect to redirects',
                })
            elif getattr(settings, "REDIRECTS_ENABLE_REGEX", False) and self.regular_expression and re.match(self.regular_expression, redirect.old_path):
                raise ValidationError({
                    'new_path': 'There is already a redirect from this URL. Please do not redirect to redirects',
                })
