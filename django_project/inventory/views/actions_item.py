from datetime import date

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from inventory.models import *



def item_open(request, item_id):
	"""
	Action to assign an opening date to an item.
	"""
	item = _get_allowed_item_or_404(request, item_id)
	
	#if the user did not select either "today" or a custom date for opening
	if not 'choice' in request.POST.keys():
		print "No Choice"
		return HttpResponseRedirect(reverse("inventory:item_detail", args=(item_id)))
	
	if request.POST['choice'] == "today":
		open_date = date.today()
	elif request.POST['choice'] == "other":
		other_date = request.POST['open_date']
		print other_date
		if other_date == '':
			return HttpResponseRedirect(reverse("inventory:item_detail", args=(item_id)))
		open_date = other_date
	else:
		return HttpResponseRedirect(reverse("inventory:item_detail", args=(item_id)))
	
	if not item.opened:
		item.opened_date = open_date
		item.save()
	
	#return HttpResponse("Opening item {}.".format(item_id))
	#return item_detail(request, item_id)
	return HttpResponseRedirect(reverse("inventory:item_detail", args=(item_id)))


def item_delete(request, item_id):
	"""
	Action to remove the specified item from the database.
	"""
	item = _get_allowed_item_or_404(request, item_id)
	
	item.delete()
	
	return HttpResponseRedirect(reverse("inventory:inventory_index"))
		


def _get_allowed_item_or_404(request, item_id):
	"""
	Attempts to retrieve an item with the given id.  If no such item exists, or
	if the requesting user does not have authority, a 404 is raised.
	"""
	item = get_object_or_404(Item, pk=item_id)
	
	#Verify the user's authority
	if item.user != request.user or not request.user.is_authenticated():
		raise Http404()
	
	return item


