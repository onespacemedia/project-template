import re
from sre_constants import error as RegexError
from urllib.parse import urlparse

from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.html import escape

from .models import Redirect


class RedirectModelForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        if getattr(settings, 'REDIRECTS_ENABLE_REGEX', False):
            if cleaned_data['regular_expression'] and 'test_path' in cleaned_data:
                try:
                    re.sub(
                        cleaned_data['old_path'],
                        cleaned_data['new_path'],
                        cleaned_data['test_path'],
                    )
                except RegexError as err:
                    raise forms.ValidationError(
                        'There was an error in your regular expression: {}'.format(err)
                    )
        return cleaned_data

    def clean_old_path(self):
        data = self.cleaned_data['old_path']

        # urlparse is extremely forgiving (or maybe URLs are just really weird).
        # There are all sorts of things that urlparse will happily parse as
        # actual URLs (with scheme, netloc, path, etc). Just pass these
        # straight through.
        if not self.cleaned_data.get('regular_expression'):
            # So let's find out if it looks something like a URL. This is
            # so rather than manually trimming the path from the URL on a page
            # on their existing site, they can just paste in the new URL.
            parsed = urlparse(data)

            if parsed.netloc and parsed.path and parsed.scheme in ['http', 'https']:
                data = parsed.path

            if not data.startswith('/'):
                raise forms.ValidationError('"From" path must either be a full URL or start with a forward slash.')

        return data

    def clean_test_path(self):
        data = self.cleaned_data['test_path']
        if getattr(settings, 'REDIRECTS_ENABLE_REGEX', False):
            if not data and self.cleaned_data['regular_expression']:
                raise forms.ValidationError(
                    'A test path is necessary to validate your regular expression.'
                )
        return data

    class Meta:
        model = Redirect
        exclude = []


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_filter = ['type']
    search_fields = ('old_path', 'new_path')

    def get_list_display(self, request):
        if getattr(settings, 'REDIRECTS_ENABLE_REGEX', False):
            return ('old_path', 'new_path', 'regular_expression', 'type', 'test_redirect')

        return ('old_path', 'new_path', 'type', 'test_redirect')

    def get_form(self, request, obj=None, **kwargs):
        kwargs["form"] = RedirectModelForm

        if not getattr(settings, 'REDIRECTS_ENABLE_REGEX', False):
            kwargs.update({
                'exclude': ['regular_expression', 'test_path']
            })
        form = super().get_form(request, obj, **kwargs)
        return form

    def test_redirect(self, obj):
        if obj.regular_expression and getattr(settings, 'REDIRECTS_ENABLE_REGEX', False):
            url = re.sub(obj.old_path, obj.new_path, obj.test_path)
        else:
            url = obj.old_path
        return '<a target="_blank" href="{}">Test</a>'.format(
            escape(url)
        )

    test_redirect.allow_tags = True
