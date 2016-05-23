"""
Contains methods for dealing with user notifications
"""
from inventory.models import Item, UserProfile


#TODO: Deprecated: move any useful functionality to the notifications app


def has_notifications(user):
	"""
	Checks to see if the provided user has outstanding notifications
	"""
	return len(get_notifications(user)) > 0


def get_notifications(user):
	"""
	Returns a list of all of the provided user's outstanding notifications
	expressed as strings.
	"""
	notifications = []
	
	_check_notifications_expired(user, notifications)
	
	return notifications


def _check_notifications_expired(user, notifications):
	"""
	If there are any expired items associated with the request's user, appends
	a relevant notification to the provided notification list.
	"""
	expired_items = Item.get_expired_items(user)
	exp_count = len(expired_items)
	
	if exp_count > 0:
		if exp_count == 1:
			notification = 'You currently have an expired item.'
		else:
			notification = 'You currently have {} expired items.'.format(exp_count)
		notifications.append(notification)

