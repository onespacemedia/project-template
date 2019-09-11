from cms.views import SearchMetaDetailMixin
from django.views.generic import DetailView, ListView

from .models import Person


class PersonListView(ListView):
    model = Person

    def get_paginate_by(self, queryset):
        return self.request.pages.current.content.per_page

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(page__page=self.request.pages.current)


class PersonView(SearchMetaDetailMixin, DetailView):
    model = Person

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(page__page=self.request.pages.current)

    def get_context_data(self, **kwargs):
        obj = kwargs.get('object')
        context = super().get_context_data()
        context['title'] = obj.browser_title or str(obj)
        return context
