from cms.views import SearchMetaDetailMixin
from django.utils.timezone import now
from django.views.generic import DetailView, ListView

from .models import Event


class EventListView(ListView):
    model = Event

    def get_queryset(self):
        qs = super(EventListView, self).get_queryset()

        return qs.filter(
            page__page=self.request.pages.current,
            end_date__gte=now()
        )


class EventDetailView(SearchMetaDetailMixin, DetailView):
    model = Event
