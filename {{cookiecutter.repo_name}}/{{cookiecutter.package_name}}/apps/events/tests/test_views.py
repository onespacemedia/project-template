from cms.apps.pages.middleware import RequestPageManager
from django.test import RequestFactory

from ..views import EventDetailView, EventListView
from ._base import EventsBaseTestCase


class EventViewsTestCase(EventsBaseTestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def test_eventlistview_get_paginate_by(self):
        view = EventListView()
        view.request = self.factory.get('/')
        view.request.pages = RequestPageManager(view.request)
        # 10 is the default, but set to 6 in _base, so we can be sure this is
        # working
        self.assertEquals(view.get_paginate_by(None), 6)

    def test_eventlistview_get_queryset(self):
        view = EventListView()
        view.request = self.factory.get('/')
        view.request.pages = RequestPageManager(view.request)
        queryset = view.get_queryset()

        # Make sure get_queryset is only showing upcoming events.
        for event in self.future_events:
            self.assertIn(event, queryset)

        # ...and isn't showing past ones.
        for event in self.past_events:
            self.assertNotIn(event, queryset)

    def test_eventdetailview_get_context_data(self):
        view = EventDetailView()
        view.request = self.factory.get(self.future_event.get_absolute_url())
        view.request.pages = RequestPageManager(view.request)
        view.object = self.future_event

        context = view.get_context_data(object=self.future_event)
        self.assertEquals(context['object'], self.future_event)
        # Make sure a proper title is being put into the context.
        self.assertEquals(context['title'], str(self.future_event))

        # Test some SEO stuff.
        self.future_event.browser_title = 'SEO test'
        self.future_event.save()

        context = view.get_context_data(object=self.future_event)
        self.assertEquals(context['title'], 'SEO test')
