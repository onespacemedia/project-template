from cms.views import SearchMetaDetailMixin
from django.views.generic import DetailView, ListView

from .models import Resource, ResourceType


class ResourceListView(ListView):
    model = Resource

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.featured_resource = None
        self.selected_type = None

    def get_paginate_by(self, queryset):
        return self.request.pages.current.content.per_page

    def get_unfiltered_queryset(self):
        qs = super().get_queryset().filter(page__page=self.request.pages.current)

        return qs

    def get_queryset(self):
        qs = self.get_unfiltered_queryset().select_related('type', 'image', 'page')
        candidates = self.get_unfiltered_queryset().order_by('-featured')

        self.featured_resource = candidates.first()

        if self.featured_resource:
            qs = qs.exclude(id=self.featured_resource.id)

        self.selected_type = self.request.GET.get('type', '')

        if self.selected_type:
            qs = qs.filter(type__slug=self.selected_type)

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        context['featured_resource'] = self.featured_resource

        context['types'] = ResourceType.objects.filter(resource__in=self.get_unfiltered_queryset()).distinct()
        context['selected_type'] = self.selected_type

        return context


class ResourceDetailView(SearchMetaDetailMixin, DetailView):
    model = Resource
