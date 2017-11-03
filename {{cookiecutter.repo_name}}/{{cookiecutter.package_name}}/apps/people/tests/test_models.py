from ..models import People, Person
from ._base import PeopleBaseTestCase


class ApplicationTestCase(PeopleBaseTestCase):

    def test_person_get_absolute_url(self):
        self.assertEqual(self.person.get_absolute_url(), '/foo-bar/')

    def test_person_str(self):
        # Try simple first-name last-name
        self.assertEqual(self.person.__str__(), 'Foo Bar')

        self.person.title = 'Mr'
        self.assertEqual(self.person.__str__(), 'Mr Foo Bar')
        self.person.middle_name = 'Baz'
        self.assertEqual(self.person.__str__(), 'Mr Foo Baz Bar')

        # Reset
        self.person.title = None
        self.person.middle_name = None

    def test_person_twitter_url(self):
        self.person.twitter = 'onespacemedia'
        self.assertEqual(self.person.twitter_url, 'https://twitter.com/onespacemedia')
