from django.test import TestCase

from .models import *


# Tests related to the population of test/demo data.

class DictionaryDataImportTest(TestCase):
	def setUp(self):
		refresh_database()
		git = DictionaryEntry(word="Jacob", definition="Some jerk.")
		git.save()
	
	
	def test_contents(self):
		matches = len(DictionaryEntry.objects.filter(word__icontains='jacob'))
		self.assertEqual(matches, 9)
