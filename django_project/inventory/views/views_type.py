"""
Views and Actions for cruding ItemType models
"""
from datetime import timedelta

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core.urlresolvers import reverse

from search.search import SearchSettings

from inventory.models import *
from inventory.type.operations import *



def index_page(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('inventory:inventory_greeter'))
	
	custom_type_list = ItemType.objects.filter(user=request.user, 
	                                          open_grocery_entry__isnull=True)
	default_type_list = ItemType.objects.filter(user=None)
	branded_type_list = ItemType.objects.filter(user=request.user,
	                                           open_grocery_entry__isnull=False)
	
	#construct dicts for context
	default_dict_list = []
	for default_type in default_type_list.order_by('name'):
		new_dict = {
			'type': default_type,
			'count': default_type.item_count_generic(request.user)
		}
		default_dict_list.append(new_dict)
	
	
	context = {
		'custom_type_list': custom_type_list.order_by('name'),
		'branded_type_list': branded_type_list.order_by('name'),
		'default_type_dict_list': default_dict_list,
	}
	
	template = 'inventory/type/index.html'
	
	return render(request, template, context)


def search_page(request):
	"""
	A page with a search box for searching all item types.
	"""
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('inventory:inventory_greeter'))
	
	
	# Search Settings for Custom Items
	
	search_fields = {'name': 'name_input_field'}
	static_search_fields = {
		'user': request.user,
		'open_grocery_entry': None,
	}
	
	search_settings_custom = SearchSettings(
		search_model=ItemType,
		field_sources=search_fields,
		static_fields=static_search_fields,
		sort_by_length_fields=search_fields.keys(),
		result_header='Custom Item Types',
		result_template='inventory/type/summary.html',
		object_label='type',
	)
	
	
	# Search Settings for Default Items
	
	search_fields = {'name': 'name_input_field'}
	static_search_fields = {
		'user': None,
	}
	
	search_settings_default = SearchSettings(
		search_model=ItemType,
		field_sources=search_fields,
		static_fields=static_search_fields,
		sort_by_length_fields=search_fields.keys(),
		result_header='Default Item Types',
		result_template='inventory/type/summary.html',
		object_label='type',
	)
	
	
	# Build the context
	
	display_names = {'name_input_field': 'Product Name or Description',}
	
	template = 'inventory/type/search.html'
	context = {
		'search_settings_custom': search_settings_custom,
		'search_settings_default': search_settings_default,
		'search_fields': display_names,
		'submit_url': request.path
	}
	
	return render(request, template, context)


def search_owned_page(request):
	"""
	A page for searching only items which are owned.
	"""
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('inventory:inventory_greeter'))
	
	
	#TODO: temporary
	raise Http404



def detail_page(request, type_key, error_messages=None):
	item_type = get_object_or_404(ItemType, pk=type_key)
	
	#if the type needs information to be completed
	if not item_type.initialized:
		redirect_url = reverse('inventory:type:modify_page', args=(item_type.id,))
		return HttpResponseRedirect(redirect_url)
	
	
	if item_type.is_custom:
		read_only = False
	else:
		read_only = True
	
	if item_type.user != None:
		if item_type.user != request.user and not request.user.is_staff:
			raise Http404
	
	if error_messages != None:
		if len(error_messages) == 0:
			error_messages = None
	
	item_list = Item.objects.filter(user=request.user, item_type=item_type)
	
	template = 'inventory/type/detail.html'
	context = {
		'type': item_type,
		'item_list': Item.objects.filter(item_type=item_type),
		'error_messages': error_messages,
		'read_only': read_only
	}
	return render(request, template, context)


#page with form for upc lookup
def upc_page(request, error_messages=None, default_value=None):
	if error_messages != None:
		if len(error_messages) == 0:
			error_messages = None
	
	template = 'inventory/type/upc_form.html'
	context = {
		'error_messages': error_messages,
		'default_value': default_value,
	}
	return render(request, template, context)



def upc_lookup(request):
	error_messages = []
	
	try:
		upc = request.POST['upc_code']
		open_grocery_entry = OpenGroceryDatabaseEntry.objects.get(product_upc=upc)
	except OpenGroceryDatabaseEntry.DoesNotExist:
		message = 'No Product with UPC code "{}".'.format(upc)
		error_messages.append(message)
	except:
		message = 'Please enter a valid 12 or 14 digit UPC.'
		error_messages.append(message)
	
	
	if len(error_messages) > 0:
		return upc_page(request, error_messages, upc_code)
	
	
	#check to see if there is already an ItemType for this user and UPC code
	try:
		item_type = ItemType.objects.get(
			user=request.user,
			open_grocery_entry=open_grocery_entry
		)
	except ItemType.DoesNotExist:
		item_type = None
	
	
	if item_type != None:
		if item_type.initialized:
			redirect_url = reverse('inventory:type:detail', args=(item_type.id,))
			return HttpResponseRedirect(redirect_url)
	else:
		#create user-specific item
		try:
			item_type = create_type(
				user=request.user,
				name=open_grocery_entry.product_name,
				needed_temperature=0,
				openable=False,
				initialized=False,
				upc=upc
			)
		except inventory.exceptions.InvalidUPCError:
			message = 'No Product with UPC code "{}".'.format(upc)
			error_messages.append(message)
	
	
	if len(error_messages) > 0:
		return upc_page(request, error_messages, upc_code)
	
	
	redirect_url = reverse('inventory:type:modify_page', args=(item_type.id,))
	return HttpResponseRedirect(redirect_url)



def create_page(request, error_messages=None):
	if error_messages != None:
		if len(error_messages) == 0:
			error_messages = None
	
	if not request.user.is_authenticated():
		raise Http404
	
	submit_url = reverse('inventory:type:create_submit')
	
	template = 'inventory/type/create.html'
	context = {
		'error_messages': error_messages,
		'submit_url': submit_url,
	}
	return render(request, template, context)



#modify page (almost identical to create page, except submits to modify url)
def modify_page(request, type_key, error_messages=None):
	item_type = get_object_or_404(ItemType, pk=type_key)
	
	if item_type.user != request.user or not request.user.is_authenticated:
		raise Http404
	
	if error_messages != None:
		if len(error_messages) == 0:
			error_messages = None
	
	submit_url = reverse('inventory:type:modify_submit', kwargs={'type_key': type_key})
	
	template = 'inventory/type/modify.html'
	context = {
		'type': item_type,
		'error_messages': error_messages,
		'submit_url': submit_url,
	}
	return render(request, template, context)



def create_submit(request):
	"""
	Note: this is only for creating or modifying custom or upc types.
	If the provided item type is None, a new one is created, otherwise,
	the provided one is modified.
	"""
	if not request.user.is_authenticated():
		raise Http404
	
	(input_data, error_messages) = _parse_type_form(request)
	
	if len(error_messages) > 0:
		return create_page(request, error_messages)
	
	
	try:
		item_type = create_type(request.user, **input_data)
	except:
		message = 'Could not create new item type.'
		error_messages.append(message)
	
	
	if len(error_messages) > 0:
		return create_page(request, error_messages)
	
	
	redirect_url = reverse('inventory:type:detail', args=(item_type.id,))
	return HttpResponseRedirect(redirect_url)



def modify_submit(request, type_key):
	if not request.user.is_authenticated():
		raise Http404
	
	(input_data, error_messages) = _parse_type_form(request)
	
	if len(error_messages) > 0:
		return modify_page(request, type_key, error_messages)
	
	
	try:
		update_type(request.user, type_key, **input_data)
	except inventory.exceptions.InvalidValueError as error:
		message = error.message
		error_messages.append(message)
	except:
		message = 'Unable to update item type.'
		error_messages.append(message)
	
	
	if len(error_messages) > 0:
		return modify_page(request, type_key, error_messages)
	
	
	redirect_url = reverse('inventory:type:detail', args=(type_key,))
	return HttpResponseRedirect(redirect_url)


def _parse_type_form(request):
	"""
	Attempts to parse a form for the creation/modification of an item type.
	Returns a tuple whose first component is a dictionary which can be used
	as a keyword argument to type.operations.modify or type.operations.create.
	The second component is an array of error messages.
	
	Note that no validity-checking of inputs is done at this level.
	"""
	input_data = {}
	error_messages = []
	
	try:
		name = request.POST['name']
		input_data['name'] = name
	except:
		message = 'Please enter a valid name.'
		error_messages.append(message)
	
	try:
		post_openable = request.POST['openable']
		if post_openable == 'yes':
			openable = True
		elif post_openable == 'no':
			openable = False
		else:
			raise Exception
		input_data['openable'] = openable
	except:
		message = 'Please specify whether the item has multiple servings'
		error_message.append(message)
	
	
	try:
		if openable:
			post_term = request.POST['open_term']
			if post_term == 'unlimited':
				open_term = None
			elif post_term == 'week':
				open_term = timedelta(weeks=1)
			elif post_term == '5day':
				open_term = timedelta(days=5)
			elif post_term == '3day':
				open_term = timedelta(days=3)
			elif post_term == 'other':
				days = int(request.POST['open_term_other'])
				open_term = timedelta(days=days)
			else:
				raise Exception
			input_data['open_expiration_term'] = open_term
	except:
		message = 'Please indicate how long the item lasts when opened'
		error_messages.append(message)
	
	
	try:
		needed_temperature = int(request.POST['refrigeration'])
		input_data['needed_temperature'] = needed_temperature
	except:
		message = 'Please indicate whether or not the item needs refrigeration'
		error_messages.append(message)
	
	
	try:
		if needed_temperature < 3:
			post_frozen = request.POST['freezable']
			if post_frozen == 'no':
				frozen_term = None
			elif post_frozen == 'yes':
				months = int(reqeust.POST['freeze_months'])
				weeks = int(request.POST['freeze_weeks'])
				days = int(request.POST['freeze_days'])
				frozen_term = timedelta(weeks=(weeks+4*months), days=days)
			else:
				raise Exception
			input_data['freezer_expiration_term'] = frozen_term
	except:
		message = 'Please indicate if the item lasts longer when frozen'
		error_messages.append(message)
	
	
	return (input_data, error_messages)



def rename_submit(request, type_key):
	
	error_messages = []
	
	try:
		new_name = request.POST['rename']
	except:
		error_messages.append('Please enter a valid name.')
	
	if len(error_messages) > 0:
		return detail_page(request, type_key, error_messages)
	
	
	try:
		update_type(request.user, type_key, name=new_name)
	except InvalidNameError as error:
		message = error.message
		error_messages.append(message)
	except:
		raise Http404
	
	if len(error_messages) > 0:
		return detail_page(request, type_key, error_messages)
	
	redirect_url = reverse('inventory:type:detail', args=(item_type.id,))
	return HttpResponseRedirect(redirect_url)



def delete_submit(request, type_key):
	try:
		delete_type(request.user, type_key)
	except:
		raise Http404
	
	redirect_url = reverse('inventory:type:index')
	return HttpResponseRedirect(redirect_url)


