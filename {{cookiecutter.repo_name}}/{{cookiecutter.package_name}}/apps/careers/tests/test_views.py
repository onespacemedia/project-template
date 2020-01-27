from cms.apps.pages.middleware import RequestPageManager
from django.test import RequestFactory

from ..views import CareerDetailView, CareerListView
from ._base import CareersBaseTestCase


class CareerViewsTestCase(CareersBaseTestCase):
    # Remember that _base.CareersBaseTestCase gives us:
    # * closed_job (a job that has closed due to closing date)
    # * closes_future_job (a job that is open because of a future closing date)
    # * job (an open job due to no closing date)
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def test_careerlistview_get_queryset(self):
        view = CareerListView()
        view.request = self.factory.get('/')
        view.request.pages = RequestPageManager(view.request)
        queryset = view.get_queryset()

        # Make sure get_queryset is obeying closing dates.
        self.assertIn(self.job, queryset)
        self.assertIn(self.closes_future_job, queryset)
        self.assertNotIn(self.closed_job, queryset)

    def test_careerdetailview_get_context_data(self):
        view = CareerDetailView()
        view.request = self.factory.get(self.job.get_absolute_url())
        view.request.pages = RequestPageManager(view.request)
        view.object = self.job

        context = view.get_context_data(object=self.job)
        self.assertEqual(context['object'], self.job)
        # Make sure a proper title is being put into the context.
        self.assertEqual(context['title'], str(self.job))

        # Test some SEO stuff.
        self.job.browser_title = 'SEO test'
        self.job.save()

        context = view.get_context_data(object=self.job)
        self.assertEqual(context['title'], 'SEO test')
