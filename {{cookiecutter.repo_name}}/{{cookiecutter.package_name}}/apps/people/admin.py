from cms.admin import PageBaseAdmin, SearchMetaBaseAdmin
from django.contrib import admin
from suit.admin import SortableModelAdmin

from .models import People, Person, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(Person)
class PersonAdmin(SortableModelAdmin, PageBaseAdmin):
    prepopulated_fields = {'slug': ['first_name', 'last_name']}

    list_display = ['__str__', 'is_online', 'order']
    list_editable = ['is_online', 'order']

    fieldsets = (
        (None, {
            'fields': ['page', 'team', 'title', 'slug'],
        }),
        ('Name information', {
            'fields': ['title', 'first_name', 'middle_name', 'last_name', 'slug']
        }),
        ('Additional information', {
            'fields': ['photo', 'job_title', 'bio', 'teams', 'order']
        }),
        ('Contact details', {
            'fields': ['email', 'linkedin_url', 'twitter_username']
        }),
        PageBaseAdmin.PUBLICATION_FIELDS,
        PageBaseAdmin.NAVIGATION_FIELDS,
        PageBaseAdmin.SEO_FIELDS,
        PageBaseAdmin.OPENGRAPH_FIELDS,
        PageBaseAdmin.OPENGRAPH_TWITTER_FIELDS,
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(PersonAdmin, self).get_form(request, obj, **kwargs)

        try:
            form.base_fields['page'].initial = People.objects.first()
        except IndexError:
            pass

        return form
