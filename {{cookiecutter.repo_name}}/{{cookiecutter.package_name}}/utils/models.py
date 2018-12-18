from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_lazy_image.templatetags.lazy_image import lazy_image
from threadlocals.threadlocals import get_current_user


class EditableMixin:
    def get_displayed_text_for_CharField(self, field_name, field_value):
        # Need to handle max_length
        context = {
            'object': self,
            'field_name': field_name,
            'field_value': field_value,
        }
        return format_html(render_to_string('editables/simple_editable.html', context))

    def get_displayed_text_for_TextField(self, field_name, field_value):
        context = {
            'object': self,
            'field_name': field_name,
            'field_value': field_value,
        }
        return format_html(render_to_string('editables/simple_editable.html', context))

    def get_displayed_text_for_AutoField(self, field_name, field_value):
        context = {
            'object': self,
            'field_name': field_name,
            'field_value': field_value,
        }
        return format_html(render_to_string('editables/simple_editable.html', context))

    def get_displayed_text_for_HtmlField(self, field_name, field_value):
        context = {
            'object': self,
            'field_name': field_name,
            'field_value': format_html(field_value),
        }
        return format_html(render_to_string('editables/wysiwyg_editable.html', context))

    def get_displayed_text_for_ImageRefField(self, field_name, field_value):
        if not field_value:
            return ''

        image = mark_safe(render_to_string('django_lazy_image/lazy-image.html', lazy_image(field_value)))
        iframe_url = reverse('admin:media_file_wysiwyg_list')
        context = {
            'object': self,
            'field_name': field_name,
            'field_value': image,
            'iframe_url': iframe_url
        }

        return format_html(render_to_string('editables/image_editable.html', context))

    def get_text_function_for_field(self, field_type):
        return {
            'AutoField': self.get_displayed_text_for_AutoField,
            'CharField': self.get_displayed_text_for_CharField,
            'TextField': self.get_displayed_text_for_TextField,

            # CMS specific
            'HtmlField': self.get_displayed_text_for_HtmlField,
            'ImageRefField': self.get_displayed_text_for_ImageRefField,
        }.get(field_type)

    def user_can_edit(self, user):
        if user.is_superuser:
            return True
        return False

    @cached_property
    def editable(self):
        fields = [{
            'name': x.name,
            'value': getattr(self, x.name),
            'type': x.get_internal_type(),
        } for x in self._meta.get_fields(include_parents=True, include_hidden=True)]
        user = get_current_user()
        out_dict = {}
        if not (user and self.user_can_edit(user)):
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
