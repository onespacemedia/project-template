from django.apps import AppConfig
from watson import search as watson


class ResourcesConfig(AppConfig):
    name = '{{ cookiecutter.package_name }}.apps.resources'

    def ready(self):
        # These imports and class definitions must be here in order to avoid
        # an 'Apps are not ready yet exception' (as sitemaps imports from
        # cms.models).

        from cms.models import PageBaseSearchAdapter
        from cms import sitemaps
        Resource = self.get_model('Resource')

        class ResourceSiteMap(sitemaps.PageBaseSitemap):
            model = Resource

            def items(self):
                return super().items().exclude(content=None)

        watson.register(Resource, adapter_cls=PageBaseSearchAdapter)
        sitemaps.register(Resource, sitemap_cls=ResourceSiteMap)
