from datetime import date

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

from inventory.models import *
from inventory.views import views, views_location

#TODO: NEEDS REFACTOR


def item_create_page(request, type_key, error_messages=None):
	if error_messages != None:
		if len(error_messages) == 0:
			error_messages = None
	
	if not request.user.is_authenticated():
		raise Http404
	
	item_type = get_object_or_404(ItemType, pk=type_key)
	if not item_type.user in [None, request.user]:
		raise Http404
	
	location_list = Location.objects.filter(user=request.user)
	
	template = 'inventory/item_add.html'
	context = {
		'error_messages': error_messages,
		'type': item_type,
		'location_list': location_list,
	}
	return render(request, template, context)


def item_create_submit(request, type_key):
	"""
	View to which item creation forms submit
	"""
	if not request.user.is_authenticated():
		raise Http404
	
	error_messages = []
	
	
	# URL scheme requires throwing a 404 at this level, so we access the database
	item_type = get_object_or_404(ItemType, pk=type_key)
	if not item_type.user in [None, request.user]:
		raise Http404
	
	
	try:
		location_id = int(request.POST['location_list'])
	except:
		message = 'Please select a valid location.'
		error_messages.append(message)
	
	
	try:
		exp_date_option = request.POST['exp_date_option']
		if exp_date_option == 'none':
			printed_expiration_date = None
		elif exp_date_option == 'date':
			date = request.POST['exp_date']
			if date == '':
				raise Exception
			else:
				printed_expiration_date = date
		else:
			raise Exception
	except:
		message = 'Please select a valid expiration date.'
		error_messages.append(message)
	
	
	
	if len(error_messages) > 0:
		return item_create_page(request, type_key, error_messages)
	
	
	#create the item
	(new_item, error_messages) = create_item(
		user=request.user,
		location_id=location_id,
		type_id=item_type.id,
		printed_expiration_date=printed_expiration_date,
	)
	
	if new_item == None:
		return item_create_page(request, type_key, error_messages)
	
	
	#redirect to the item's detail page
	redirect_url = reverse('inventory:item_detail', args=(new_item.id,))
	return HttpResponseRedirect(redirect_url)


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
	
	return HttpResponseRedirect(reverse("inventory:item_detail", args=(item_id,)))


def item_move_page(request, item_id, error_messages=None):
	if error_messages != None:
		if len(error_messages) == 0:
			error_messages = None
	
	item = _get_allowed_item_or_404(request, item_id)
	
	location_list = Location.objects.filter(user=request.user)
	
	template = 'inventory/item_move.html'
	context = {
		'error_messages': error_messages,
		'item': item,
		'location_list': location_list,
	}
	return render(request, template, context)


def item_move_submit(request, item_id):
	"""
	Changes the storage location of an item
	"""
	item = _get_allowed_item_or_404(request, item_id)
	
	error_messages = []
	
	try:
		location_id = int(request.POST['location_list'])
		location = Location.objects.get(pk=location_id)
		if location.user != request.user:
			raise Exception
	except:
		message = 'Please select a valid location.'
		error_messages.append(message)
	
	if len(error_messages) > 0:
		return item_move_page(request, item_id, error_messages)
	
	item.location = location
	item.save()
	
	redirect_url = reverse('inventory:item_detail', args=(item_id,))
	return HttpResponseRedirect(redirect_url)


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


