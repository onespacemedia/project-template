from cms.views import PageDetailMixin
from django.views.generic import DetailView, ListView

from .models import Career


class CareerListView(ListView):
    model = Career

    def get_paginate_by(self, queryset):
        return self.request.pages.current.content.per_page

    def get_queryset(self):
        queryset = super().get_queryset()
        # Only show the careers with either no closing date or a closing date
        # that is not in the past, and that are assigned to the current
        # page.
        return queryset.select_open().filter(
            page__page=self.request.pages.current
        )


class CareerDetailView(PageDetailMixin, DetailView):
    model = Career
