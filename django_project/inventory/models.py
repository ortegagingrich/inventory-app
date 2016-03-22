from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class Location(models.Model):
	name = models.CharField(max_length = 100)
	refrigerated = models.BooleanField(default = False)
	frozen = models.BooleanField(default = False)
	
	def __str__(self):
		return self.name


class ItemType(models.Model):
	name = models.CharField(max_length = 50)
	openable = models.BooleanField(default = False)
	open_expiration_term = models.DurationField()
	
	def __str__(self):
		return self.name


class Item(models.Model):
	item_type = models.ForeignKey(ItemType, on_delete = models.CASCADE)
	location = models.ForeignKey(Location, on_delete = models.CASCADE)
	
	printed_expiration_date = models.DateField(blank=True)
	opened_date = models.DateField(null=True, blank=True)
	
	def __str__(self):
		return self.item_type.name



def __test__():
	print "inventory models test"

if __name__ == '__main__':
	__test__()
