from datetime import timedelta

from cms.apps.pages.models import Page
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils import timezone
from watson import search

from ..models import Category, Event, Events


class EventsBaseTestCase(TestCase):

    def setUp(self):
        # Note: as this is the only page in the database, it's absolute URL
        # will simply be '/'
        with search.update_index():
            content_type = ContentType.objects.get_for_model(Events)
            self.page = Page.objects.create(
                content_type=content_type,
                title='Test events',
                slug='test-events',
            )

            self.events_page = Events.objects.create(
                page=self.page,
                per_page=6,
            )

            self.category = Category(title='Test category')

        self.future_events = []
        # Add a few future dates.
        for i in range(0, 6):
            self.future_events.append(Event.objects.create(
                page=self.events_page,
                slug='test-future-{}'.format(i + 1),
                title='Test future {}'.format(i + 1),
                start_date=(timezone.now() + timedelta(days=i)).date(),
                end_date=(timezone.now() + timedelta(days=i + 5)).date(),
            ))

        # Standalone test for Event model methods.
        self.future_event = self.future_events[0]

        self.past_events = []
        # Add some past dates.
        for i in range(1, 3):
            self.past_events.append(Event.objects.create(
                page=self.events_page,
                slug='test-past-{}'.format(i),
                title='Test past {}'.format(i),
                start_date=(timezone.now() - timedelta(days=i + 1)).date(),
                end_date=(timezone.now() - timedelta(days=i)).date(),
            ))
