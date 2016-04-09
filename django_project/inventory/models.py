from __future__ import unicode_literals

from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class Location(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
	
	name = models.CharField(max_length=100)
	refrigerated = models.BooleanField(default=False)
	frozen = models.BooleanField(default=False)
	
	def create_from_default(user, default_location):
		"""
		Creates a new Location using the provided default location, saves it to
		the database and returns it.
		"""
		n = default_location.name
		r = default_location.refrigerated
		f = default_location.frozen
		new_location = Location(user=user, name=n, refrigerated=r, frozen=f)
		new_location.save()
		return new_location
	
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


class OpenGroceryDatabaseEntry(models.Model):
	grp_id = models.IntegerField()
	product_brand = models.CharField(max_length = 50)
	product_name = models.CharField(max_length = 100)
	product_upc = models.BigIntegerField()
	


class ItemType(models.Model):
	open_grocery_entry = models.ForeignKey(OpenGroceryDatabaseEntry,
	                           on_delete = models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
	name = models.CharField(max_length = 50)
	openable = models.BooleanField(default = False)
	
	open_expiration_term = models.DurationField(null=True, blank=True)
	freezer_expiration_term = models.DurationField(null=True, blank=True)
	
	def __str__(self):
		return self.name


class Item(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	
	item_type = models.ForeignKey(ItemType, on_delete = models.CASCADE)
	location = models.ForeignKey(Location, on_delete = models.CASCADE)
	
	printed_expiration_date = models.DateField(blank=True)
	opened_date = models.DateField(null=True, blank=True)
	
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
		modified_date = self.printed_expiration_date
		
		if self.item_type.openable and self.opened:
			base_date = self.opened_date
			term = self.item_type.open_expiration_term
			modified_date = min(base_date + term, modified_date)
		
		return min(self.printed_expiration_date, modified_date)
	
	def __str__(self):
		return self.item_type.name



def __test__():
	print "inventory models test"

if __name__ == '__main__':
	__test__()
