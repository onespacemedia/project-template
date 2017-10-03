from cms.admin import SearchMetaBaseAdmin
from django.contrib import admin
from suit.admin import SortableModelAdmin

from .models import People, Person, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(Person)
class PersonAdmin(SortableModelAdmin, SearchMetaBaseAdmin):
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
            'fields': ['email', 'linkedin_url', 'twitter_username']
        }),
        SearchMetaBaseAdmin.PUBLICATION_FIELDS,
        SearchMetaBaseAdmin.SEO_FIELDS,
        SearchMetaBaseAdmin.OPENGRAPH_FIELDS,
        SearchMetaBaseAdmin.OPENGRAPH_TWITTER_FIELDS,
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        try:
            form.base_fields['page'].initial = People.objects.first()
        except IndexError:
            pass

        return form
