"""
Module of methods for the creation of default database entries (i.e. locations,
item types, etc.) for e.g. new users and for updating changes to the defaults.
"""

from inventory.models import *


"""
Methods for Creating user defaults
"""


def create_user_defaults(user):
	"""
	Creates all default database entries for the specified user.  This should
	be called whenever a new user is created.
	"""
	create_user_default_locations(user)
	create_user_default_types(user)


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


def create_user_default_types(user):
	pass


def _dangerous_temporary_complete_reset_of_defaults():
	#TODO: delete this method once default system/models stabilize
	"""
	For experimental purposes only!  Purges the database (!!!) and generates new
	defaults for all non-staff users.
	"""
	from django.contrib.auth.models import User
	
	from inventory.user.purge import purge_database_user
	
	for user in User.objects.all():
		if not user.is_staff:
			purge_database_user(user)
			create_user_defaults(user)
