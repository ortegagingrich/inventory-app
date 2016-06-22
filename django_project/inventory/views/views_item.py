from datetime import date, timedelta

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic

from inventory.models import *
from inventory.item.operations import *
from inventory.views import views_location, views_user
import inventory.exceptions



def index_page(request, order_by_expiration=False):
	if not request.user.is_authenticated():
		redirect_url = reverse('inventory:inventory_greeter')
		return HttpResponseRedirect(redirect_url)
	
	# Get the queryset
	if request.user.is_staff and False:
		itemset = Item.objects.all().order_by('item_type__name').order_by('user')
	else:
		itemset = Item.objects.filter(user=request.user)
		itemset = itemset.order_by('item_type__name')
	
	if order_by_expiration:
		itemset = itemset.order_by('printed_expiration_date')
	
	
	template = 'inventory/inventory_index.html'
	context = {
		'item_list': itemset,
	}
	return render(request, template, context)


def item_index_expired(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('inventory:inventory_greeter'))
	
	queryset = Item.objects.filter(user=request.user)
	item_list = []
	for item in queryset.order_by('item_type__name'):
		if item.expired:
			item_list.append(item)
	
	template = 'inventory/inventory_index_expired.html'
	context = {
		'item_list': item_list,
	}
	
	return render(request, template, context)


def item_index_old(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('inventory:inventory_greeter'))
	
	queryset = Item.objects.filter(user=request.user)
	item_list = []
	for item in queryset.order_by('item_type__name'):
		if item.soon_to_expire:
			item_list.append(item)
	
	template = 'inventory/inventory_index_old.html'
	context = {
		'item_list': item_list,
	}
	
	return render(request, template, context)


class ItemDetailView(generic.DetailView):
	model = Item
	template_name = 'inventory/item_detail.html'
	
	def dispatch(self, request, *args, **kwargs):
		item = get_object_or_404(Item, pk=kwargs['pk'])
		owner = item.user
		if request.user != owner and not request.user.is_staff:
			redirect_url = request.get_full_path()
			return views_user.login_page(request, redirect_url=redirect_url)
		return super(ItemDetailView, self).dispatch(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super(ItemDetailView, self).get_context_data(**kwargs)
		#print context
		return context




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
	
	
	# Extract data from the form
	try:
		location_id = int(request.POST['location_list'])
		location = Location.objects.get(pk=location_id)
	except:
		location = None
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
	
	# Make sure that the proposed storage location has an acceptable temperature
	if location != None:
		if not location.frozen:
			if item_type.needed_temperature == 3:
				message = 'This item must be frozen.  Please select a frozen storage location.'
				error_messages.append(message)
			elif item_type.needed_temperature == 2 and not location.refrigerated:
				message = 'This item requires refrigeration but the location '
				message += 'you selected is not refrigerated.'
				error_messages.append(message)
	
	
	if len(error_messages) > 0:
		return item_create_page(request, type_key, error_messages)
	
	
	# Try to create the item using the form data extracted above
	try:
		new_item = create_item(			
			user=request.user,
			location_id=location_id,
			type_id=item_type.id,
			printed_expiration_date=printed_expiration_date,
		)
	except inventory.exceptions.InvalidValueError as error:
		message = error.message
		error_messages.append(message)
	except:
		message = 'Could not create item.'
		error_messages.append(message)
	
	
	if len(error_messages) > 0:
		return item_create_page(request, type_key, error_messages)
	
	
	# Redirect to the item's detail page
	redirect_url = reverse('inventory:item_detail', args=(new_item.id,))
	return HttpResponseRedirect(redirect_url)



def item_open_page(request, item_id, error_messages = None):
	item = get_object_or_404(Item, pk=item_id)
	if request.user != item.user or not request.user.is_authenticated():
		raise Http404
	
	if error_messages != None:
		if len(error_messages) == 0:
			error_messages = None
	
	refrigerated_list = Location.objects.filter(user=request.user)
	refrigerated_list = refrigerated_list.filter(Q(refrigerated=True) | Q(frozen=True))
	
	template = 'inventory/item_open.html'
	context = {
		'item': item,
		'error_messages': error_messages,
		'location_list': refrigerated_list
	}
	return render(request, template, context)


def item_open_submit(request, item_id):
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
				
			elif refrigerator_choice == 'new':
				# call the location create view to process the sub-form
				(location, location_errors) = views_location.create_location(request)
				if location != None:
					if location.refrigerated or location.forzeon:
						location_id = location.id
					else:
						message = 'The item is still not in a refrigerated location.'
						error_messages.append(message)
				else:
					error_messages += location_errors
			else:
				raise Exception
			
			
			move_item(request.user, item_id, location_id)
		except:
			message = 'Please choose a refrigerated location to move this item to.'
			error_messages.append(message)
	
	
	#if the user did not select either "today" or a custom date for opening
	if not 'choice' in request.POST.keys():
		message = 'Please select the date upon which this item was opened.'
		error_messages.append(message)
	
	if request.POST['choice'] == "today":
		open_date = date.today()
	elif request.POST['choice'] == 'yesterday':
		open_date = date.today() - timedelta(days=1)
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
		return item_open_page(request, item_id, error_messages)
	
	
	try:
		open_item(request.user, item.id, open_date)
	except inventory.exceptions.InvalidValueError as error:
		message = error.value
		error_messages.append(message)
	
	
	if len(error_messages) > 0:
		return item_open_page(request, item_id, error_messages)
	
	
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
	except:
		message = 'Please select a valid location.'
		error_messages.append(message)
	
	if len(error_messages) > 0:
		return item_move_page(request, item_id, error_messages)
	
	
	try:
		move_item(request.user, item_id, location_id)
	except inventory.exceptions.InvalidValueError as error:
		message = error.message
		error_messages.append(message)
	except:
		message = 'Unable to move item.'
		error_messages.append(message)
	
	if len(error_messages) > 0:
		return item_move_page(request, item_id, error_messages)
	
	
	redirect_url = reverse('inventory:item_detail', args=(item_id,))
	return HttpResponseRedirect(redirect_url)


def item_delete_submit(request, item_id):
	"""
	Action to remove the specified item from the database.
	"""
	try:
		delete_item(request.user, item_id)
	except:
		raise Http404
	
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

