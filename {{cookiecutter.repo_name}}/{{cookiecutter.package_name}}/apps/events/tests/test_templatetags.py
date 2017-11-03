from ..templatetags.events import get_events_list_url, get_upcoming_events
from ._base import EventsBaseTestCase


class EventsModelsTestCase(EventsBaseTestCase):
    def test_get_events_list_url(self):
        self.assertEqual(get_events_list_url(), self.page.get_absolute_url())

    # Ensure upcoming events are only showing upcoming events and are not
    # including past ones.
    def test_get_upcoming_events(self):
        upcoming = list(get_upcoming_events(count=4))
        self.assertEqual(upcoming, self.future_events[:4])
        for event in self.past_events:
            self.assertNotIn(event, upcoming)
