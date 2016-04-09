from inventory.models import *


def purge_database_user(target_user):
	"""
	Purges all database entries associated with the provided user and returns
	a collection of the entries purged
	"""
	
	items = Item.objects.filter(user=target_user)
	types = ItemType.objects.filter(user=target_user)
	locations = Location.objects.filter(user=target_user)
	
	#Purge items
	items.delete()
	types.delete()
	locations.delete()
	
	purged = []
	purged += items
	purged += types
	purged += locations
	
	return purged
