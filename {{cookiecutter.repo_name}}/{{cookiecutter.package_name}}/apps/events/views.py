from cms.views import SearchMetaDetailMixin
from django.views.generic import DetailView, ListView

from .models import Event


class BaseEventListView(ListView):
    model = Event

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.featured_event = None

    def get_paginate_by(self, queryset):
        return self.request.pages.current.content.per_page

    def get_unfiltered_queryset(self):
        return super().get_queryset().filter(
            page__page=self.request.pages.current,
        )

    def get_queryset(self):
        qs = self.get_unfiltered_queryset().order_by('end_date')
        candidates = self.get_unfiltered_queryset().order_by('-featured', 'end_date')

        self.featured_event = candidates.first()

        if self.featured_event:
            qs = qs.exclude(id=self.featured_event.id)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['featured_event'] = self.featured_event

        return context


class PastEventListView(BaseEventListView):
    def get_unfiltered_queryset(self):
        return super().get_unfiltered_queryset().select_past()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['switcher_text'] = 'View upcoming events'
        context['switcher_url'] = self.request.pages.current.get_absolute_url()
        context['hero_title'] = self.request.pages.current.content.hero_title_past or self.request.pages.current.content.hero_title

        return context


class UpcomingEventListView(BaseEventListView):
    def get_unfiltered_queryset(self):
        return super().get_unfiltered_queryset().select_upcoming()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['switcher_text'] = 'View past events'
        context['switcher_url'] = self.request.pages.current.reverse('event_list_past')
        context['hero_title'] = self.request.pages.current.content.hero_title

        return context


class EventDetailView(SearchMetaDetailMixin, DetailView):
    model = Event
