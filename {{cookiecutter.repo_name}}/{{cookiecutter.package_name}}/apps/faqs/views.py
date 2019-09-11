from django.views.generic import DetailView, ListView

from .models import Faq


class FaqListView(ListView):
    model = Faq

    def get_paginate_by(self, queryset):
        return self.request.pages.current.content.per_page

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(page__page=self.request.pages.current)


class FaqView(DetailView):
    model = Faq
