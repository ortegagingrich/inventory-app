"""
Contains functions to attempt to create/modify user accounts.
"""
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from inventory.user import defaults
import inventory.exceptions


def create_user(username, email, fname=None, lname=None):
	"""
	Attempts to create a user using the provided information.
	"""
	
	try:
		validate_email(email)
	except ValidationError:
		raise inventory.exceptions.InvalidEmailError(email)
	
	
	#Next, check to make sure that the username meets the criteria
	if len(username) < 5:
		raise inventory.exceptions.InvalidUsernameError(username)
	elif User.objects.filter(username=username).exists():
		raise inventory.exceptions.UnavailableUsernameError(username)
	
	
	
	#TODO: better temporary password
	temporary_password = 'password'
	
	#build the account object
	try:
		user = User.objects.create_user(username, email, temporary_password)
		defaults.create_user_defaults(user)
	except:
		raise inventory.exceptions.UserCreateError
	
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


def change_password(user, tentative_password):
	"""
	Attempts to change the user's password.
	"""
	error_messages = []
	
	if len(tentative_password) < 6:
		raise inventory.exceptions.InvalidPasswordError(password)
	
	#change password
	request.user.set_password(tentative_password)
	request.user.save()


