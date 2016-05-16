"""
Contains functions for carrying out CRUD operations.  Views CHANGE (but not read)
the database through these functions
"""
from django.http import HTTP404

from inventory.models import Item, Location, ItemType
import inventory.exceptions


def create_item(user, location_id, type_id, printed_expiration_date):
	"""
	Attempts to create a new item.
	"""
	
	try:
		location = Location.objects.get(pk=location_id)
		if location.user != user:
			raise Exception
	except:
		raise inventory.exceptions.InvalidLocationError(location_id)
	
	try:
		item_type = ItemType.objects.get(pk=type_id)
		if item_type.user != user:
			raise Exception
	except:
		raise inventory.exceptions.InvalidItemTypeError(type_id)
	
	
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
	pass



def _get_allowed_item_or_404(user, item_id):
	"""
	Attempts to retrieve an item with the given id.  If no such item exists, or
	if the requesting user does not have authority, a 404 is raised.
	"""
	item = get_object_or_404(Item, pk=item_id)
	
	#Verify the user's authority
	if item.user != user or not user.is_authenticated():
		raise Http404
	
	return item
