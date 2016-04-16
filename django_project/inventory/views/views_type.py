"""
Views and Actions for cruding ItemType models
"""
from datetime import timedelta

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core.urlresolvers import reverse

from inventory.models import *


def index_page(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('inventory:inventory_greeter'))
	
	custom_type_list = ItemType.objects.filter(user=request.user, 
	                                          open_grocery_entry__isnull=True)
	default_type_list = ItemType.objects.filter(user=None)
	branded_type_list = ItemType.objects.filter(user=request.user,
	                                           open_grocery_entry__isnull=False)
	
	template = 'inventory/type/index.html'
	context = {
		'custom_type_list': custom_type_list.order_by('name'),
		'default_type_list': default_type_list.order_by('name'),
		'branded_type_list': branded_type_list.order_by('name'),
	}
	return render(request, template, context)


#detail view
def detail_page(request, type_key, error_messages=None):
	item_type = get_object_or_404(ItemType, pk=type_key)
	
	
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


#create page
def create_page(request, error_messages=None):
	if error_messages != None:
		if len(error_messages) == 0:
			error_messages = None
	
	if not request.user.is_authenticated():
		raise Http404
	
	template = 'inventory/type/create.html'
	context = {
		'error_messages': error_messages,
	}
	return render(request, template, context)


#create
def create_submit(request):
	"""
	Note: this is only for creating custom types
	"""
	if not request.user.is_authenticated():
		raise Http404
	
	error_messages = []
	
	try:
		name = request.POST['name']
		if len(name) < 1:
			message = 'Cannot give item type name "{}".  '
			message += 'Item Type names must have at least one character.'
			error_messages.append(message.format(name))
		elif '\'' in name or '\"' in name:
			message = "Names cannot contain apostrophes or quotations."
			error_messages.append(message)
	except:
		error_messages.append('Please enter a valid name.')
	
	if not 'openable' in request.POST.keys():
		error_messages.append("Please specify whether the item has multiple servings.")
		openable = False
	else:
		post_openable = request.POST['openable']
		if post_openable == 'yes':
			openable = True
		elif post_openable == 'no':
			openable = False
		else:
			error_messages.append("Please specify whether the item has multiple servings.")
	
	open_term = None
	if openable:
		if not 'open_term' in request.POST.keys():
			message = 'Please indicate how long the item lasts when opened'
			error_messages.append(message)
		else:
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
				try:
					days = int(request.POST['open_term_other'])
					open_term = timedelta(days=days)
				except:
					message = 'Please indicate how long the item lasts when opened'
					error_messages.append(message)
			else:
				message = 'Please indicate how long the item lasts when opened'
				error_messages.append(message)
	
	try:
		needed_temperature = int(request.POST['refrigeration'])
	except:
		message = 'Please indicate whether or not the item needs refrigeration'
		error_messages.append(message)
		needed_temperature = None
	
	
	if needed_temperature == 3:
		frozen_term = None
	elif needed_temperature != None:
		try:
			post_frozen = request.POST['freezable']
			if post_frozen == 'no':
				frozen_term = None
			elif post_frozen == 'yes':
				print('here1')
				months = int(request.POST['freeze_months'])
				weeks = int(request.POST['freeze_weeks'])
				days = int(request.POST['freeze_days'])
				frozen_term = timedelta(weeks=(weeks+4*months), days=days)
				print(frozen_term)
			else:
				raise Exception
		except:
			message = 'Please indicate if the item lasts longer when frozen'
			error_messages.append(message)
	
	
	
	if len(error_messages) > 0:
		return create_page(request, error_messages)
	
	
	item_type = ItemType(
		user = request.user,
		name = name,
		needed_temperature = needed_temperature,
		openable = openable,
		open_expiration_term = open_term,
		freezer_expiration_term = frozen_term,
	)
	
	item_type.save()
	
	redirect_url = reverse('inventory:type:detail', args=(item_type.id,))
	return HttpResponseRedirect(redirect_url)


#rename
def rename_submit(request, type_key):
	item_type = get_object_or_404(ItemType, pk=type_key)
	
	if item_type.user != request.user and not request.user.is_staff:
		raise Http404
	elif not item_type.is_generic:
		raise Http404
	
	error_messages = []
	
	try:
		new_name = request.POST['rename']
		
		if len(new_name) < 1:
			message = 'Cannot rename item type "{}" to "{}".  '
			message += 'Location names must have at least one character.'
			error_messages.append(message.format(location.name, new_name))
		elif '\'' in new_name or '\"' in new_name:
			message = "Names cannot contain apostrophes or quotations."
			error_messages.append(message)
		else:
			item_type.name = new_name
			item_type.save()
	except:
		error_messages.append('Please enter a valid name.')
	
	if len(error_messages) > 0:
		return detail_page(request, type_key, error_messages)
	else:
		redirect_url = reverse('inventory:type:detail', args=(item_type.id,))
		return HttpResponseRedirect(redirect_url)


#delete
def delete_submit(request, type_key):
	item_type = get_object_or_404(ItemType, pk=type_key)
	
	if request.user != item_type.user or not request.user.is_authenticated():
		raise Http404
	
	item_type.delete()
	
	redirect_url = reverse('inventory:type:index')
	return HttpResponseRedirect(redirect_url)


