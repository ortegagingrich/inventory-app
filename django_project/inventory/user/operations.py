"""
Contains functions to attempt to create/modify user accounts.
"""
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

from inventory.user import defaults
import inventory.exceptions
import inventory.email


def create_user(username, email, fname=None, lname=None):
	"""
	Attempts to create a user using the provided information.
	"""
	
	
	
	
	#Next, check to make sure that the username meets the criteria
	if len(username) < 5:
		raise inventory.exceptions.InvalidUsernameError(username)
	elif User.objects.filter(username=username).exists():
		raise inventory.exceptions.UnavailableUsernameError(username)
	
	
	try:
		validate_email(email)
	except ValidationError:
		raise inventory.exceptions.InvalidEmailError(email)
	
	
	#build the account object
	try:
		user = User.objects.create_user(username, email, 'thou art a knave')
		defaults.create_user_defaults(user)
	except:
		raise inventory.exceptions.UserCreateError
	
	#this will fail if the provided email is invalid
	try:
		temporary_password = reset_password(user)
	except Exception as exception:
		#Did not work out, delete the user
		user.delete()
		raise exception
	
	
	return user


def update_user(user, email=None, fname=None, lname=None):
	"""
	Attempts to execute the provided updates to the provided user.
	"""
	if email != None:
		try:
			validate_email(email)
			user.email = email
		except ValidationError:
			raise inventory.exceptions.InvalidEmailError(email)
	if fname != None:
		user.first_name = fname
	if lname != None:
		user.last_name = lname
	
	user.save()


CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
def reset_password(user):
	"""
	Generates a randomly generated temporary password and sends it to the user's
	email address.
	"""
	temporary_password = get_random_string(15, CHARS)
	change_password(user, temporary_password)
	
	inventory.email.send_temporary_password(user, temporary_password)
	
	return temporary_password


def change_password(user, tentative_password):
	"""
	Attempts to change the user's password.
	"""
	
	if len(tentative_password) < 6:
		raise inventory.exceptions.InvalidPasswordError(password)
	
	#change password
	user.set_password(tentative_password)
	user.save()


