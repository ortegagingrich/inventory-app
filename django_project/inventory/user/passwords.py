"""
Methods related to user password operations
"""
from django.core.exceptions import ObjectDoesNotExist

from inventory.models import UserProfile



def needs_reset(user):
	"""Checks to see if the provided user needs a password reset"""
	try:
		profile = UserProfile.objects.get(user=user)
		return profile._needs_password_reset
	except ObjectDoesNotExist:
		return False


def on_reset(user):
	"""
	User no longer needs to reset password
	"""
	try:
		profile = UserProfile.objects.get(user=user)
		profile._needs_password_reset = False
		profile.save()
	except ObjectDoesNotExist:
		pass


def on_require_reset(user):
	"""
	User does something that requires a password reset (e.g. new account)
	"""
	profile, new = UserProfile.objects.get_or_create(user=user)

	if not profile._needs_password_reset:
		profile._needs_password_reset = True
		profile.save()
