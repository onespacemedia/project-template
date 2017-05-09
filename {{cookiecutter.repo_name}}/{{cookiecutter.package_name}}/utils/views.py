from django.views.generic import TemplateView


class FrontendView(TemplateView):
    def get_template_names(self):
        # If no slug exists just serve the base so we can access the template switcher
        template_name = self.kwargs.get('slug', '_base')

        return ['frontend/{}.html'.format(template_name)]
