"""
Contains functions for carrying out CRUD operations.  Views CHANGE (but not read)
the database through these functions
"""
import django.core.exceptions

from inventory.models import Item, Location, ItemType
import inventory.exceptions


def create_item(user, location_id, type_id, printed_expiration_date):
	"""
	Attempts to create a new item.
	"""
	
	location = Location.retrieve_with_write_permission(user, location_id)
	item_type = ItemType.retrieve_with_write_permission(user, type_id)
	
	
	#create the item
	try:
		new_item = Item(user=user,
			location=location,
			item_type=item_type,
			printed_expiration_date=printed_expiration_date,
		)
		new_item.save()
	except django.core.exceptions.ValidationError:
		raise inventory.exceptions.InvalidDateError(printed_expiration_date)
	except:
		raise inventory.exceptions.ItemCreateError
	
	return new_item


def open_item(user, item_id, open_date):
	"""
	Attempts to open the provided item, provided that it is not already open.
	"""
	item = Item.retrieve_with_write_permission(user, item_id)
	
	#if already opened, do nothing
	if item.opened:
		return
	
	try:
		item.opened_date = open_date
		item.save()
	except django.core.exceptions.ValidationError:
		raise inventory.exceptions.InvalidDateError(open_date)
	


def move_item(user, item_id, location_id):
	"""
	Attempts to move an item with the specified id to a location with the
	specified id.
	"""
	item = Item.retrieve_with_write_permission(user, item_id)
	location = Location.retrieve_with_write_permission(user, location_id)
	
	item.location = location
	item.save()


def delete_item(user, item_id):
	"""
	Attempts to delete the item with the specified id, provided that the provided
	user is its owner
	"""
	item = Item.retrieve_with_write_permission(user, item_id)
	
	item.delete()



