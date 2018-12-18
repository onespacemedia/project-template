import json
import re

from cms.apps.media.models import File
from django.apps import apps
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import TemplateView
from django_lazy_image.templatetags.lazy_image import lazy_image


class FrontendView(TemplateView):
    def get_template_names(self):
        # If no slug exists just serve the base so we can access the template switcher
        template_name = self.kwargs.get('slug', '_base')

        return ['frontend/{}.html'.format(template_name)]


class FrontendEditView(View):
    def post(self, request):
        if not request.user.is_superuser:
            return JsonResponse({'success': False})

        data = json.loads(request.body.decode('utf-8'))

        app_name = data['app']
        model_name = data['model']
        pk = data['pk']
        field = data['field']
        value = data['value']

        model = apps.get_model(app_label=app_name, model_name=model_name)

        if field and not model._meta.get_field(field).get_internal_type() == 'HtmlField':
            value = strip_tags(re.sub('<br>', '\n', value))

        if field and model._meta.get_field(field).get_internal_type() == 'ImageRefField':
            value = File.objects.get(pk=value)

        candidate = model.objects.filter(pk=pk).first()
        setattr(candidate, field, value)
        candidate.save()

        return JsonResponse({'success': True})


class RenderLazyImageView(View):
    def get(self, request):
        if not request.user.is_superuser:
            return JsonResponse({'success': False})

        image_pk = request.GET['pk']

        image = File.objects.get(pk=image_pk)
        image_html = mark_safe(render_to_string('django_lazy_image/lazy-image.html', lazy_image(image)))

        return JsonResponse({'success': True, 'image_html': image_html})

