from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from notifications.models import NotificationModel


def delete_notification(request, key):
	"""
	View for deleting the notification with the specified id (provided the user
	is allowed to do so) and redirecting to the provided redirection url.
	"""
	if not request.user.is_authenticated():
		raise Http404
	
	try:
		redirect_url = request.POST['redirect_url']
		print redirect_url
	except:
		raise Http404
	try:
		failure_url = request.POST['failure_url']
	except:
		failure_url = redirect_url
	
	try:
		notification = get_object_or_404(NotificationModel, pk=key, user=request.user)
		notification.delete()
	except:
		return HttpResponseRedirect(failure_url)
	
	return HttpResponseRedirect(redirect_url)
