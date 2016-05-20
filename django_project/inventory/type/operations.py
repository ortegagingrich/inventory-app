"""
Contains functions for carrying out CRUD operations.  Views CHANGE (but not read)
the database through these functions
"""
import django.core.exceptions

from inventory.models import ItemType, OpenGroceryDatabaseEntry
import inventory.exceptions


def create_type(user, name, needed_temperature, openable, open_expiration_term=None,
                freezer_expiration_term=None, initialized=True, upc=None):
	_validate_name(name)
	_validate_temperature(needed_temperature)
	
	if upc != None:
		try:
			open_grocery_entry = OpenGroceryDatabaseEntry.objects.get(product_upc=upc)
		except OpenGroceryDatabaseEntry.DoesNotExist:
			raise inventory.exceptions.InvalidUPCError
	else:
		open_grocery_entry = None
	
	try:
		item_type = ItemType(
			user=user,
			name=name,
			needed_temperature=needed_temperature,
			openable=openable,
			open_expiration_term=open_expiration_term,
			freezer_expiration_term=freezer_expiration_term,
			initialized=initialized,
			open_grocery_entry=open_grocery_entry,
		)
		item_type.save()
	except:
		raise inventory.exceptions.ItemTypeCreateError
	
	return item_type


def update_type(user, type_id, name=None, needed_temperature=None, openable=None,
                open_expiration_term=-1, freezer_expiration_term=-1, initialized=True):
	# Note that the default values of open_expiration_term and freezer_expiration
	# term are -1 instead of None because these variables might actually be
	# null-valued and we must distinguish between a call which wishes to set
	# one of these to None and one which wants to leave the current value.
	item_type = ItemType.retrieve_with_write_permission(user, type_id)
	
	if name != None:
		_validate_name(name)
		item_type.name = name
	if needed_temperature != None:
		_validate_temperature(needed_temperature)
		item_type.needed_temperature = needed_temperature
	if openable != None:
		item_type.openable = openable
	if open_expiration_term != -1:
		item_type.open_expiration_term = open_expiration_term
	if freezer_expiration_term != -1:
		item_type.freezer_expiration_term = freezer_expiration_term
	item_type.initialized = initialized
	
	item_type.save()


def delete_type(user, type_id):
	item_type = ItemType.retrieve_with_write_permission(user, type_id)
	
	item_type.delete()



def _validate_name(name):
	"""
	Checks to see whether the name provided is suitable.  If not, it raises an
	InvalidNameException
	"""
	if len(name) < 1 or '\'' in name or '\"' in name:
		raise inventory.exceptions.InvalidNameError(name)

def _validate_temperature(temp):
	"""
	Checks to make sure that the provided storage type temperature is valid
	"""
	if temp < 0 or temp > 3:
		raise inventory.exceptions.InvalidValueError(temp)

	
