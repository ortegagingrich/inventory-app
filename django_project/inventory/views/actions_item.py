from datetime import date

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from inventory.models import *
from inventory.views import views, views_location



def item_open(request, item_id):
	"""
	Action to assign an opening date to an item.
	"""
	item = _get_allowed_item_or_404(request, item_id)
	
	error_messages = []
	
	
	#change of location, if needed
	if item.item_type.needed_temperature == 1 and not item.location.refrigerated:
		try:
			refrigerator_choice = request.POST['refrigerator']
			if refrigerator_choice == 'existing':
				location_id = int(request.POST['location_list'])
				item.location = Location.objects.get(pk=location_id)
				item.save()
			elif refrigerator_choice == 'new':
				(location, location_errors) = views_location.create_location(request)
				if location != None:
					item.location = location
					item.save()
					if not (location.refrigerated or location.frozen):
						message = 'The item is still not in a refrigerated location.'
						error_messages.append(message)
				else:
					error_messages += location_errors
			else:
				raise Exception
			
		except:
			message = 'Please choose a refrigerated location to move this item to.'
			error_messages.append(message)
	
	
	#if the user did not select either "today" or a custom date for opening
	if not 'choice' in request.POST.keys():
		message = 'Please select the date upon which this item was opened.'
		error_messages.append(message)
	
	if request.POST['choice'] == "today":
		open_date = date.today()
	elif request.POST['choice'] == "other":
		other_date = request.POST['open_date']
		if other_date == '':
			message = 'Please select the date upon which this item was opened.'
			error_messages.append(message)
		open_date = other_date
	else:
		message = 'Please select the date upon which this item was opened.'
		error_messages.append(message)
	
	
	if len(error_messages) > 0:
		return views.item_open_page(request, item_id, error_messages)
	
	
	if not item.opened:
		item.opened_date = open_date
		item.save()
	
	#return HttpResponse("Opening item {}.".format(item_id))
	#return item_detail(request, item_id)
	return HttpResponseRedirect(reverse("inventory:item_detail", args=(item_id,)))


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
		raise Http404
	
	return item


