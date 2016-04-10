"""
Module of methods for the creation of default database entries (i.e. locations,
item types, etc.) for e.g. new users and for updating changes to the defaults.
"""

from inventory.models import *

def update_all_defaults():
	"""
	Updates all default database entries.
	
	Should not be called too often; performance scales very poorly with the size
	of the userbase.
	"""
	update_all_default_locations()
	#TODO: update other defaults


def update_all_default_locations():
	"""
	Calls update_default_location for all default locations.
	
	Should not be called too often; performance scales very poorly with the size
	of the userbase.
	"""
	for default_location in LocationDefault.objects.all():
		update_default_location(default_location)


def update_default_location(default_location):
	"""
	Searches for all location objects in the database with the specified
	location as a default template.  Every field marked as unmodified by the
	user is updated to the current value of the corresponding default.
	
	This should be called whenever a default location is modified e.g. by an
	admin.
	"""
	default_set = Location.objects.filter(default=default_location)
	for location in default_set:
		#If location.name_default is None, the field was added since the last update.
		if location.name_default in [location.name, None]:
			location.name = default_location.name
			location.name_default = default_location.name
		location.save()


"""
Methods for Creating user defaults
"""

def _dangerous_temporary_complete_reset_of_defaults():
	#TODO: delete this method once default system/models stabilize
	"""
	For debugging purposes only!  Purges the database (!!!) and generates new
	defaults for all non-staff users.
	"""
	from django.contrib.auth.models import User
	
	from inventory.user.purge import purge_database_user
	
	for user in User.objects.all():
		if not user.is_staff:
			purge_database_user(user)
			create_user_defaults(user)


def create_user_defaults(user):
	"""
	Creates all default database entries for the specified user.  This should
	be called whenever a new user is created.
	"""
	create_user_default_locations(user)


def create_user_default_locations(user):
	"""
	Creates a copy of each 'default' location specific to the target user and
	adds it to the database.
	"""
	for default in LocationDefault.objects.all():
		n = default.name
		r = default.refrigerated
		f = default.frozen
		location = Location(user=user, name=n, refrigerated=r, frozen=f)
		location.default = default
		location.name_default = default.name
		location.save()
