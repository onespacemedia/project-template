from datetime import date

from ..models import Event
from ._base import EventsBaseTestCase


class EventsModelsTestCase(EventsBaseTestCase):
    def test_category_meta(self):
        # Make sure categories isn't being pluralised as 'categorys'.
        self.assertEqual(self.category._meta.verbose_name_plural, 'categories')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test category')

    # Ensure select_upcoming is pulling all future dates and no past ones.
    def test_eventsqueryset_select_upcoming(self):
        future = Event.objects.select_upcoming()
        for event in self.future_events:
            self.assertIn(event, future)
        for event in self.past_events:
            self.assertNotIn(event, future)

    # Ensure select_past is doing the inverse of the above.
    def test_eventsqueryset_select_past(self):
        past = Event.objects.select_past()
        for event in self.past_events:
            self.assertIn(event, past)
        for event in self.future_events:
            self.assertNotIn(event, past)

    def test_events_str(self):
        self.assertEqual(str(self.events_page), 'Test events')

    def test_event_str(self):
        self.assertEqual(str(self.future_event), 'Test future 1')

    def test_events_get_absolute_url(self):
        self.assertEqual(self.future_event.get_absolute_url(), '/test-future-1/')

    def test_event_date(self):
        # Test formatted date.
        date_test = Event(
            start_date=date(2017, 1, 1),
            end_date=date(2017, 1, 1),
        )
        self.assertEquals(date_test.date, '1 January 2017')

        date_test = Event(
            start_date=date(2017, 1, 1),
            end_date=date(2017, 11, 11),
        )
        self.assertEquals(date_test.date, '1 January 2017 - 11 November 2017')
