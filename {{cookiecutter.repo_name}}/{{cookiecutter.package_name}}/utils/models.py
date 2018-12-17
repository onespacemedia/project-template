from __future__ import print_function

from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django_lazy_image.templatetags.lazy_image import lazy_image
from threadlocals.threadlocals import get_current_user


class EditableMixin:
    def get_displayed_text_for_CharField(self, field_name, field_value):
        # Need to handle max_length
        return mark_safe(f'<span class="js-SimpleEditable" data-pk="{self.pk}" data-field="{field_name}" data-app="{self._meta.app_label}" data-model="{self._meta.object_name}" contentEditable>{field_value}</span>')

    def get_displayed_text_for_TextField(self, field_name, field_value):
        return mark_safe(f'<span class="js-SimpleEditable" data-pk="{self.pk}" data-field="{field_name}" data-app="{self._meta.app_label}" data-model="{self._meta.object_name}" contentEditable>{field_value}</span>')

    def get_displayed_text_for_AutoField(self, field_name, field_value):
        return mark_safe(f'<span class="js-SimpleEditable" data-pk="{self.pk}" data-field="{field_name}" data-app="{self._meta.app_label}" data-model="{self._meta.object_name}" contentEditable>{field_value}</span>')

    def get_displayed_text_for_HtmlField(self, field_name, field_value):
        return mark_safe(f'<span class="js-WYSIWYGEditable" data-pk="{self.pk}" data-field="{field_name}" data-app="{self._meta.app_label}" data-model="{self._meta.object_name}" id="{self._meta.app_label}-{self._meta.object_name}-{self.pk}-{field_name}">{field_value}</span>')

    def get_displayed_text_for_ImageRefField(self, field_name, field_value):
        if field_value:
            image = mark_safe(render_to_string('django_lazy_image/lazy-image.html', lazy_image(field_value)))
            upload_url = reverse('admin:media_file_wysiwyg_list')
            return mark_safe(f'<span class="js-ImageEditable" data-url="{upload_url}" data-pk="{self.pk}" data-field="{field_name}" data-app="{self._meta.app_label}" data-model="{self._meta.object_name}">{image}</span>')
        return ''

    def get_text_function_for_field(self, field_type):
        return {
            'AutoField': self.get_displayed_text_for_AutoField,
            'CharField': self.get_displayed_text_for_CharField,
            'TextField': self.get_displayed_text_for_TextField,

            # CMS specific
            'HtmlField': self.get_displayed_text_for_HtmlField,
            'ImageRefField': self.get_displayed_text_for_ImageRefField,
        }.get(field_type)

    @cached_property
    def editable(self):
        fields = [{
            'name': x.name,
            'value': getattr(self, x.name),
            'type': x.get_internal_type(),
        } for x in self._meta.get_fields(include_parents=True, include_hidden=True)]
        user = get_current_user()
        out_dict = {}
        if not (user and user.is_superuser):
            for field in fields:
                if not field['type'] == 'ImageRefField':
                    value = field['value']
                else:
                    if field['value']:
                        value = mark_safe(render_to_string('django_lazy_image/lazy-image.html', lazy_image(field['value'])))
                    else:
                        value = ''
                out_dict[field['name']] = value
        else:
            for field in fields:
                text_function = self.get_text_function_for_field(field['type'])
                if text_function:
                    out_dict[field['name']] = text_function(field['name'], field['value'])
                else:
                    out_dict[field['name']] = field['value']
        return out_dict
