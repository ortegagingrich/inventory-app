"""
Contains methods for setting up contexts for notifications.
"""
from django.http import Http404
from django.shortcuts import render


def notification_page(request):
	"""A view for a notification page"""
	if not request.user.is_authenticated():
		raise Http404
	
	template = 'inventory/notifications.html'
	context = {}
	
	return render(request, template, context)


