"""
Contains functions for carrying out CRUD operations.  Views CHANGE (but not read)
the database through these functions
"""
from inventory.models import *
import inventory.exceptions



def create_location(user, name, frozen, refrigerated):
	"""
	Attempts to return a new location using the given request.
	"""
	
	_validate_name(name)
	
	try:
		location = Location(
			user=user,
			name=name,
			frozen=frozen,
			refrigerated=refrigerated,
		)
		location.save()
	except:
		raise inventory.exceptions.LocationCreateError
	
	return location


def rename_location(user, location_id, name):
	"""
	Attempts to rename the location with the specified id owned by the provided
	user, provided that such a location exists and the name is valid.
	"""
	location = Location.retrieve_with_write_permission(user, location_id)
	_validate_name(name)
	
	location.name = name
	location.save()


def delete_location(user, location_id):
	"""
	Attempts to delete the location with the specified id, provided that the provided
	user is its owner
	"""
	location = Location.retrieve_with_write_permission(user, location_id)
	
	location.delete()


def _validate_name(name):
	"""
	Checks to see whether the name provided is suitable.  If not, it raises an
	InvalidNameException
	"""
	if len(name) < 1 or '\'' in name or '\"' in name:
		raise inventory.exceptions.InvalidNameError(name)
	

