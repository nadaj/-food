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

        smore_results_1 = len(self.search_engine.find('smore'))
        smore_results_2 = len(self.search_engine.find("s'more"))
        self.assertTrue(smore_results_1 == smore_results_2)

        icecream_results_1 = len(self.search_engine.find('icecream'))
        icecream_results_2 = len(self.search_engine.find('ice-cream'))
        icecream_results_3 = len(self.search_engine.find('ice cream'))
        icecream_results_4 = len(self.search_engine.find('ice_cream'))
        self.assertTrue(icecream_results_1 == icecream_results_2 == icecream_results_3 == icecream_results_4)

