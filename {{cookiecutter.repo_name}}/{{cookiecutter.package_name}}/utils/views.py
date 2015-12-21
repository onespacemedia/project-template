from django.views.generic import TemplateView


class FrontendView(TemplateView):
    def get_template_names(self, *args, **kwargs):
        return ['frontend/{}.html'.format(self.kwargs['slug'])]
