from cms.apps.pages.middleware import RequestPageManager
from django.test import RequestFactory

from ..views import ResourceDetailView, ResourceListView
from ._base import ResourcesBaseTestCase


class ResourcesViewsTestCase(ResourcesBaseTestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def test_resourcelistview_get_queryset(self):
        view = ResourceListView()
        view.request = self.factory.get('/')
        view.request.pages = RequestPageManager(view.request)
        queryset = view.get_unfiltered_queryset()

        self.assertIn(self.whitepaper, queryset)
        self.assertIn(self.case_study, queryset)
        self.assertIn(self.video, queryset)

    def test_resourcedetailview_get_context_data(self):
        view = ResourceDetailView()
        view.request = self.factory.get(self.case_study.get_absolute_url())
        view.request.pages = RequestPageManager(view.request)
        view.object = self.case_study

        context = view.get_context_data(object=self.case_study)
        self.assertEqual(context['object'], self.case_study)
        self.assertEqual(context['title'], str(self.case_study))

        # Test some SEO stuff.
        self.case_study.browser_title = 'SEO test'
        self.case_study.save()

        context = view.get_context_data(object=self.case_study)
        self.assertEqual(context['title'], 'SEO test')
