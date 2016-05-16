"""
Custom exceptions for the inventory app
"""

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


class InvalidDateError(Exception):
	"""
	Exceptions resulting from invalid dates
	"""
	def __init__(self, bad_date, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)
		self.bad_date = bad_date



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


