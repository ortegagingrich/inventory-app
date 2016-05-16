"""
Contains methods for setting up contexts for notifications.
"""
from django.http import Http404
from django.shortcuts import render

from inventory.user.notifications import get_notifications



def notification_page(request):
	"""A view for a notification page"""
	if not request.user.is_authenticated():
		raise Http404
	
	notifications = get_notifications(request.user)
	
	template = 'inventory/notifications.html'
	context = {
		'notification_count': len(notifications),
		'notifications': notifications,
	}
	
	return render(request, template, context)


