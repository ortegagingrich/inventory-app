"""
Contains functions for carrying out CRUD operations.  Views CHANGE (but not read)
the database through these functions
"""
from inventory.models import Item, Location, ItemType


def create_item(user, location_id, type_id, printed_expiration_date):
	"""
	Attempts to create a new item.  Returns the item and a list of error messages.
	"""
	error_messages = []
	
	
	try:
		location = Location.objects.get(pk=location_id)
		if location.user != user:
			raise Exception
	except:
		location = None
		message = 'Invalid Location ID: {}'
		error_messages.append(message.format(location_id))
	
	try:
		item_type = ItemType.objects.get(pk=type_id)
		if item_type.user != user:
			raise Exception
	except:
		item_type = None
		messages = 'Invalid ItemType ID: {}'
		error_messages.append(messages.format(type_id))
	
	
	if location == None or item_type == None:
		return (None, error_messages)
	
	
	#create the item
	try:
		new_item = Item(user=user,
			location=location,
			item_type=item_type,
			printed_expiration_date=printed_expiration_date,
		)
		new_item.save()
	except:
		new_item = None
		message = 'Could not create item.'
		error_messages.append(message)
	
	return (new_item, error_messages)
