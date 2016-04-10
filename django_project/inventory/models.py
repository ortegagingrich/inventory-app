from __future__ import unicode_literals

from datetime import date, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

""" Locations """

class LocationDefault(models.Model):
	"""
	Class of default locations which serve as 'blueprints' for user-specific
	locations.
	"""
	
	name = models.CharField(max_length=100)
	refrigerated = models.BooleanField(default=False)
	frozen = models.BooleanField(default=False)
	
	@property
	def temperature(self):
		if self.frozen:
			return 'Frozen'
		elif self.refrigerated:
			return 'Refrigerated'
		else:
			return "Room Temperature"
	
	def __str__(self):
		return self.name


class Location(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	default = models.ForeignKey(LocationDefault, null=True, default=None,
	                            on_delete=models.SET_DEFAULT)
	
	name = models.CharField(max_length=100)
	name_default = models.CharField(max_length=100, null=True, default=None)
	
	refrigerated = models.BooleanField(default=False)
	
	frozen = models.BooleanField(default=False)
	
	@property
	def temperature(self):
		if self.frozen:
			return "Frozen"
		elif self.refrigerated:
			return "Refrigerated"
		else:
			return "Room Temperature"
	
	def __str__(self):
		return self.name

""" Item Types """

class OpenGroceryDatabaseEntry(models.Model):
	grp_id = models.IntegerField()
	product_brand = models.CharField(max_length = 50)
	product_name = models.CharField(max_length = 100)
	product_upc = models.BigIntegerField()
	

class ItemTypeDefault(models.Model):
	"""
	Class of default item types which serve as 'blueprints' for user-specific
	item types.  Note that these are for non-upc items only.
	"""
	pass


class ItemType(models.Model):
	open_grocery_entry = models.ForeignKey(OpenGroceryDatabaseEntry,
	                           on_delete = models.CASCADE, null=True, blank=True)
	user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
	
	
	name = models.CharField(max_length = 50)
	
	"""
	needed_temperature values:
		0: Does not need to be refrigerated
		1: Only needs refrigeration when opened
		2: Always needs refrigeration
		3: Always needs to be frozen
	"""
	needed_temperature = models.SmallIntegerField(default=2)
	
	openable = models.BooleanField(default = False)
	open_expiration_term = models.DurationField(null=True, blank=True)
	freezer_expiration_term = models.DurationField(null=True, blank=True)
	
	@property
	def is_generic(self):
		return open_grocery_entry == None
	
	def __str__(self):
		return self.name

""" Items """

class Item(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	
	location = models.ForeignKey(Location, on_delete = models.CASCADE)
	item_type = models.ForeignKey(ItemType, on_delete = models.CASCADE)
	
	
	
	printed_expiration_date = models.DateField(blank=True)
	opened_date = models.DateField(null=True, blank=True)
	
	#Do not change these; they are handled automatically:
	#indicates that at some point, the item was improperly stored.
	_improperly_stored = models.BooleanField(default=False)
	#the date when the item was placed in its last location; if null
	_location_date = models.DateField(null=True)
	
	
	def __setattr__(self, k, v):
		super(Item, self).__setattr__(k, v)
		if k in ['location_id', 'opened_date']:
			self.on_state_change()
	
	@property
	def improperly_stored(self):
		return self._improperly_stored
	
	@property
	def expired(self):
		return date.today() > self.expiration_date
	
	@property
	def opened(self):
		return self.opened_date != None
	
	@property
	def expiration_date(self):
		"""
		Computes the actual expiration date, assuming the item is stored in its
		current conditions indefinitely.
		"""
		
		#first, check for immediate disqualifications (improper storage)
		if self._improperly_stored:
			return min(self._location_date, date.today()) - timedelta(days=1)
		
		
		modified_date = self.printed_expiration_date
		
		
		if self.item_type.openable and self.opened:
			base_date = self.opened_date
			term = self.item_type.open_expiration_term
			modified_date = min(base_date + term, modified_date)
		
		return min(self.printed_expiration_date, modified_date)
	
	
	def on_state_change(self):
		"""
		Executed whenever an item is opened or moved to a new location.
		"""
		#Note: the part below might fail for new objects just being created.
		try:
			self._location_date = date.today()
			self.check_improper_storage()
		except:
			pass
	
	
	def check_improper_storage(self):
		"""
		Checks to see if the item is currently improperly stored.  This should
		be called whenever the item's location is changed.
		"""
		if self._location_date == None:
			self._location_date = date.today()
		
		if not self._improperly_stored:
			if self.item_type.needed_temperature in [1, 2]: #needs refrigeration
				if not self.location.refrigerated or self.location.frozen:
					if self.item_type.needed_temperature == 2:
						self._improperly_stored = True
					elif self.opened:
						self._improperly_stored = True
			elif self.item_type.needed_temperature == 3: #needs freezer
				if not self.location.frozen:
					self._improperly_stored = True
		
		self.save()
	
	def __str__(self):
		return self.item_type.name



def __test__():
	print "inventory models test"

if __name__ == '__main__':
	__test__()
