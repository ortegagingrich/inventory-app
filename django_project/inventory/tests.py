import datetime

from django.test import TestCase

from .models import Item, ItemType


class QuestionMethodTests(TestCase):
	
	def test_expire_open_limited(self):
		"""
		Items opened more than the safe term for their type should be shown as
		expired, regardless of the printed expiration date.
		"""
		
		term = datetime.timedelta(days=7)
		item_type = ItemType(name="test", openable=True, open_expiration_term=term)
		
		today = datetime.date.today()
		open_date = today - datetime.timedelta(days=8)
		exp_date = today + datetime.timedelta(days=2)
		item = Item(item_type=item_type, printed_expiration_date=exp_date,
		            opened_date=open_date)
		
		self.assertEqual(item.expired, True)
	
	def test_expire_date_limited(self):
		"""
		Items expire on the date, even if they have been open less than the
		safe term for their type.
		"""
		
		term = datetime.timedelta(days=7)
		item_type = ItemType(name="test", openable=True, open_expiration_term=term)
		
		today = datetime.date.today()
		open_date = today - datetime.timedelta(days=2)
		exp_date = today - datetime.timedelta(days=1)
		item = Item(item_type=item_type, printed_expiration_date=exp_date,
		            opened_date=open_date)
		
		self.assertEqual(item.expired, True)
	
	def test_open_not_expired(self):
		"""
		Items are good before the printed date as long as they have been open
		for a shorter duration than the safe term of their type.
		"""
		term = datetime.timedelta(days=7)
		item_type = ItemType(name="test", openable=True, open_expiration_term=term)
		
		today = datetime.date.today()
		open_date = today - datetime.timedelta(days=2)
		exp_date = today + datetime.timedelta(days=5)
		item = Item(item_type=item_type, printed_expiration_date=exp_date,
		            opened_date=open_date)
		
		self.assertEqual(item.expired, False)
	
	def test_not_opened(self):
		"""
		Items that are not opened expire on the printed expiration date.
		"""
		term = datetime.timedelta(days=7)
		item_type = ItemType(name="test", openable=True, open_expiration_term=term)
		
		today = datetime.date.today()
		open_date = None
		exp_date = today + datetime.timedelta(days=1)
		item = Item(item_type=item_type, printed_expiration_date=exp_date,
		            opened_date=open_date)
		
		self.assertEqual(item.expired, False)


