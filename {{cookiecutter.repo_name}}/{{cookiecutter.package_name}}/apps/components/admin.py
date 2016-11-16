from django.contrib import admin
from django.core.urlresolvers import reverse

from .models import CallToAction


# @admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin):
    list_display = ['title', 'pages_used_on']

    def pages_used_on(self, obj):
        pages_used = []

        for rel in obj._meta.related_objects:
            for page in getattr(obj, rel.get_accessor_name()).all():
                pages_used.append(
                    '<a href="{}">{}</a>'.format(
                        '{}#id_call_to_action'.format(
                            reverse('admin:pages_page_change', args=[page.page.id])
                        ),
                        page
                    )
                )

        return ', '.join(pages_used)

    pages_used_on.short_description = 'Pages used on'
    pages_used_on.allow_tags = True
