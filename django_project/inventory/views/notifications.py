"""
Contains methods for setting up contexts for notifications.
"""
from django.http import Http404
from django.shortcuts import render

from inventory.models import Item, UserProfile

#TODO: DEAL WITH LATER

def notifications_view(request):
	"""A view for a notification page"""
	if not request.user.is_authenticated():
		raise Http404
	
	template = 'inventory/notifications.html'
	context = _get_notifications_context(request)
	
	return render(request, template, context)


def _get_notifications_context(request):
	"""
	Returns a dictionary with all notifications for the provided request.
	"""
	notifications = get_notifications(request.user)
	
	context = {
		'notification_count': len(notifications),
		'notifications': notifications,
	}
	
	return context


def has_notifications(user):
	return len(get_notifications(user)) > 0


def get_notifications(user):
	notifications = []
	
	_check_notifications_account(user, notifications)
	_check_notifications_expired(user, notifications)
	
	return notifications


def _check_notifications_account(user, notifications):
	"""
	If there are any notifications related to the user's account (e.g. needs a
	password reset, etc.), appends them to the provided notification list
	"""
	if UserProfile.needs_reset(user):
		notification = 'You must reset your password.'
		notifications.append(notification)


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

