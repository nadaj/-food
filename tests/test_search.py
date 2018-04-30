from food.services.search_service import SearchEngine
from django.test import TestCase


class SearchTestCase(TestCase):
    """
        Note:
        - Data for database: py manage.py dumpdata -e sessions -e admin -e contenttypes -o food/fixtures/database.json
        - Run tests: py manage.py test tests --settings=food.settings.tests
    """

    fixtures = ['database.json']

    def setUp(self):
        self.search_engine = SearchEngine()
        SearchEngine.init_cached_keywords()

    def test_search_input(self):
        self.assertIsNotNone(self.search_engine.find('cereals'))
        self.assertIsNotNone(self.search_engine.find('cereal'))

        self.assertIsNotNone(self.search_engine.find('smore'))
        self.assertIsNotNone(self.search_engine.find("s'more"))
