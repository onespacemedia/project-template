from django.views.generic import DetailView, ListView

from .models import Career


class CareerListView(ListView):
    model = Career

    def get_paginate_by(self, queryset):
        return self.request.pages.current.content.per_page

    def get_queryset(self):
        queryset = super(CareerListView, self).get_queryset()

        return queryset.filter(page__page=self.request.pages.current)


class CareerDetailView(DetailView):
    model = Career
