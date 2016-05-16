"""
Contains functions for carrying out CRUD operations.  Views CHANGE (but not read)
the database through these functions
"""

from inventory.models import Item, Location, ItemType
import inventory.exceptions


def create_item(user, location_id, type_id, printed_expiration_date):
	"""
	Attempts to create a new item.
	"""
	
	location = _retrieve_location(user, location_id)
	item_type = _retrieve_type(user, type_id)
	
	
	#create the item
	try:
		new_item = Item(user=user,
			location=location,
			item_type=item_type,
			printed_expiration_date=printed_expiration_date,
		)
		new_item.save()
	except:
		raise inventory.exceptions.ItemCreateError
	
	return new_item


def open_item():
	"""
	Attempts to open the provided item.
	"""
	pass


def move_item(user, item_id, location_id):
	"""
	Attempts to move an item with the specified id to a location with the
	specified id.
	"""
	item = _retrieve_item(user, item_id)
	location = _retrieve_location(user, location_id)
	
	item.location = location
	item.save()






def _retrieve_item(user, item_id):
	"""
	Attempts to retrieve an item with the given id belonging to the given user.
	If no such item exists, the appropriate error is raised
	"""
	try:
		item = Item.objects.get(pk=item_id)
		if item.user != user:
			raise Exception
	except:
		raise inventory.exceptions.InvalidItemError(item_id)
	return item


def _retrieve_type(user, type_id):
	"""
	Attempts to retrieve an ItemType with the given id belonging to the given user.
	If no such type exists, the appropriate error is raised
	"""
	try:
		item_type = ItemType.objects.get(pk=type_id)
		if not item_type.user in [user, None]:
			raise Exception
	except:
		raise inventory.exceptions.InvalidItemTypeError(type_id)
	return item_type


def _retrieve_location(user, location_id):
	"""
	Attempts to retrieve a location with the given id belonging to the given user.
	If no such location exists, the appropriate error is raised
	"""
	try:
		location = Location.objects.get(pk=location_id)
		if location.user != user:
			raise Exception
	except:
		raise inventory.exceptions.InvalidLocationError(location_id)
	return location



