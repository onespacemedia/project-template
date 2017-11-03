from cms.apps.pages.middleware import RequestPageManager
from cms.apps.pages.models import Page
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory
from watson import search

from ..models import People
from ..views import PersonView, PersonListView
from ._base import PeopleBaseTestCase


class PeopleViewsTestCase(PeopleBaseTestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        with search.update_index():
            content_type = ContentType.objects.get_for_model(People)
            self.extra_page = Page.objects.create(
                content_type=content_type,
                title='Extra',
                slug='extra',
                parent=self.page,
            )

            self.extra_person_page = People.objects.create(
                page=self.extra_page,
            )

    def test_list_get_queryset(self):
        view = PersonListView()
        view.request = self.factory.get('/')
        view.request.pages = RequestPageManager(view.request)

        objects = view.get_queryset()
        self.assertIn(self.person, objects)

        # Make sure page filtering is working.
        view.request = self.factory.get('/extra/')
        view.request.pages = RequestPageManager(view.request)
        objects = view.get_queryset()
        self.assertNotIn(self.person, objects)

    def test_list_get_paginate_by(self):
        view = PersonListView()
        view.request = self.factory.get('/')
        view.request.pages = RequestPageManager(view.request)
        view.request.pages.current.content.per_page = 7

        self.assertEquals(view.get_paginate_by(view.get_queryset()), 7)

    def test_detail_get_context_data(self):
        view = PersonView()
        view.request = self.factory.get('/foo-bar/')
        view.request.pages = RequestPageManager(view.request)
        view.kwargs = {'slug': self.person.slug}
        view.object = view.get_object()
        context = view.get_context_data(object=view.object)

        # Make sure a proper title is in the context.
        self.assertEquals(context['title'], 'Foo Bar')

        self.person.browser_title = 'Browser Title'
        context = view.get_context_data(object=self.person)
        self.assertEquals(context['title'], 'Browser Title')
