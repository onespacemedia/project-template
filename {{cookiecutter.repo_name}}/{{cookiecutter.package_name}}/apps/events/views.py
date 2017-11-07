from cms.views import SearchMetaDetailMixin
from django.views.generic import DetailView, ListView

from .models import Event


class EventListView(ListView):
    model = Event

    def get_paginate_by(self, queryset):
        return self.request.pages.current.content.per_page

    def get_queryset(self):
        qs = super(EventListView, self).get_queryset()

        return qs.filter(
            page__page=self.request.pages.current,
        ).select_upcoming().order_by('end_date')


class EventDetailView(SearchMetaDetailMixin, DetailView):
    model = Event
