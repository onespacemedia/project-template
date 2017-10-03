from urllib.parse import urlparse

from cms.admin import SearchMetaBaseAdmin
from django import forms
from django.contrib import admin
from suit.admin import SortableModelAdmin

from .models import People, Person, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }


class PersonForm(forms.ModelForm):
    '''A form that is forgiving of "errors" in the Twitter and LinkedIn fields.
    The `twitter` field will be normalised to an @-less username, and `linkedin`
    will be normalised to a URL.'''

    def clean_linkedin(self):
        value = self.cleaned_data.get('linkedin')
        if not value:
            return value

        # Let them provide @onespacemedia (not sure if this form is really in
        # use on LinkedIn)
        if value.startswith('@'):
            return 'https://www.linkedin.com/in/{}'.format(value[1:])

        # See if it looks anything like a URL.
        url_prefixes = ['http:', 'https:', 'www.linkedin.com', 'linkedin.com']

        if any([value.startswith(prefix) for prefix in url_prefixes]):
            if not value.startswith('https:') and not value.startswith('http:'):
                return 'https://{}'.format(value)
            return value

        return 'https://www.linkedin.com/in/{}'.format(value)

    def clean_twitter(self):
        value = self.cleaned_data.get('twitter')
        if not value:
            return value
        # Let them provide @onespacemedia
        if value.startswith('@'):
            return value[1:]
        # Let's see if they have provided us with something that looks a bit
        # like a URL.
        url_prefixes = ['http:', 'https:', 'www.twitter.com', 'm.twitter.com', 'twitter.com']

        if not any([value.startswith(prefix) for prefix in url_prefixes]):
            # It's not a URL, so it's probably just a username as we want it
            # to be.
            return value

        # OK, so it looks sort of like a URL. Do they have a protocol part?
        url = value
        if not url.startswith('http:') and not url.startswith('https:'):
            url = 'https://{}'.format(url)
        try:
            return urlparse(url).path[1:]
        except ValueError:
            raise forms.ValidationError('Please provide either a username or a URL.')


@admin.register(Person)
class PersonAdmin(SortableModelAdmin, SearchMetaBaseAdmin):
    form = PersonForm

    prepopulated_fields = {'slug': ['first_name', 'last_name']}

    list_display = ['__str__', 'is_online']
    list_editable = ['is_online', 'order']
    list_filter = list(SearchMetaBaseAdmin.list_filter) + ['team']

    fieldsets = (
        (None, {
            'fields': ['page'],
        }),
        ('Name information', {
            'fields': ['title', 'first_name', 'middle_name', 'last_name', 'slug']
        }),
        ('Profile', {
            'fields': ['photo', 'job_title', 'bio', 'team']
        }),
        ('Contact details', {
            'fields': ['email', 'linkedin', 'twitter']
        }),
        SearchMetaBaseAdmin.PUBLICATION_FIELDS,
        SearchMetaBaseAdmin.SEO_FIELDS,
        SearchMetaBaseAdmin.OPENGRAPH_FIELDS,
        SearchMetaBaseAdmin.OPENGRAPH_TWITTER_FIELDS,
    )

    def aget_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        try:
            form.base_fields['page'].initial = People.objects.first()
        except IndexError:
            pass

        return form
