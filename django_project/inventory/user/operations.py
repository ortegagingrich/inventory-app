"""
Contains functions to attempt to create/modify user accounts.
"""
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from inventory.user import defaults


def create_user(username, email, fname=None, lname=None):
	"""
	Attempts to create a user using the provided information.  Returns the new
	user or None as well as a list of error messages
	"""
	error_messages = []
	
	try:
		validate_email(email)
	except ValidationError:
		error_messages.append('Please enter a valid email address.')
	
	
	#Next, check to make sure that the username meets the criteria
	if len(username) < 5:
		error_messages.append('Please enter a username with at least five characters.')
	elif User.objects.filter(username=username).exists():
		message = 'The username "{}" is already taken.  Please choose another.'
		error_messages.append(message.format(username))
	
	
	#if there are errors, do not continue
	if len(error_messages) > 0:
		return (None, error_messages)
	
	
	#TODO: better temporary password
	temporary_password = 'password'
	
	#build the account object
	try:
		user = User.objects.create_user(username, email, temporary_password)
		defaults.create_user_defaults(user)
	except:
		user = None
		return error_messages.append('Could not create account.  Please try again.')
	
	return (user, error_messages)


def update_user(user, email=None, fname=None, lname=None):
	"""
	Attempts to execute the provided updates to the provided user.  Returns
	a list of error messages
	"""
	if email != None:
		validate_email(email)
		user.email = email
	if fname != None:
		user.first_name = fname
	if lname != None:
		user.last_name = lname
	
	user.save()


def change_password(user, tentative_password):
	"""
	Attempts to change the user's password.  Returns a list of error messages
	"""
	error_messages = []
	
	if len(tentative_password) < 6:
		error_messages.append('Passwords must have at least 6 characters.')
	
	if len(error_messages) == 0:
		#change password
		request.user.set_password(tentative_password)
		request.user.save()
	
	return error_messages


