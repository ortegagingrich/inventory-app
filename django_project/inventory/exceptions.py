"""
Custom exceptions for the inventory app
"""

# Item ID errors

class InvalidIDError(Exception):
	"""
	Exceptions resulting from invalid object IDs
	"""
	def __init__(self, bad_id, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)
		self.bad_id = bad_id

class InvalidLocationError(InvalidIDError):
	pass

class InvalidItemTypeError(InvalidIDError):
	pass

class InvalidItemError(InvalidIDError):
	pass


# Invalid Value errors

class InvalidValueError(Exception):
	"""
	Exceptions resulting from some sort of invalid value
	"""
	value_descriptor = 'value'
	requirements_message = ''
	
	def __init__(self, bad_value=None, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)
		self.bad_value = bad_value
	
	def __getattr__(self, name):
		value_name = 'bad_{}'.format(type(self).value_descriptor)
		if name == value_name:
			return self.bad_value
		
		return Exception.__getattribute__(self, name)
	
	@property
	def message(self):
		message = '"{}" is not a valid {}.  ' + type(self).requirements_message
		value_descriptor = type(self).value_descriptor
		return message.format(self.bad_value, value_descriptor)


class InvalidDateError(InvalidValueError):
	value_descriptor = "date"

class InvalidEmailError(Exception):
	value_descriptor = "email"

class InvalidPasswordError(InvalidValueError):
	value_descriptor = 'password'
	requirements_message = 'Valid passwords must contain at least 6 characters.'

class InvalidNameError(InvalidValueError):
	value_descriptor = 'name'
	requirements_message = """
	Valid names must contain at least 1 character and cannot contain apostrophes
	or quotes.
	"""

class InvalidUsernameError(InvalidValueError):
	value_descriptor = 'username'
	requirements_message = 'Valid usernames must contain at least 5 characters.'

class UnavailableUsernameError(InvalidUsernameError):
	@property
	def message(self):
		message = 'The username "{}" is not available.'
		return message.format(self.bad_username)


# Generic Creation Errors

class ObjectCreateError(Exception):
	"""
	Exceptions raised when the objects are not created properly
	"""
	pass

class LocationCreateError(ObjectCreateError):
	pass

class ItemTypeCreateError(ObjectCreateError):
	pass

class ItemCreateError(ObjectCreateError):
	pass

class UserCreateError(ObjectCreateError):
	pass


