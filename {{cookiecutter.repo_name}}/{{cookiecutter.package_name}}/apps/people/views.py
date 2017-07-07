from django.views.generic import DetailView, ListView

from .models import Person


class PersonListView(ListView):
    model = Person

    def get_paginate_by(self, queryset):
        return self.request.pages.current.content.per_page

    def get_queryset(self):
        queryset = super(PersonListView, self).get_queryset()

        return queryset.filter(page__page=self.request.pages.current)


class PersonView(DetailView):
    model = Person
