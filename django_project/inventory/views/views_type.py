"""
Views and Actions for cruding ItemType models
"""

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
		'custom_type_list': custom_type_list,
		'default_type_list': default_type_list,
		'branded_type_list': branded_type_list,
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


def delete_submit(request, type_key):
	item_type = get_object_or_404(ItemType, pk=type_key)
	
	if request.user != item_type.user or not request.user.is_authenticated():
		raise Http404
	
	item_type.delete()
	
	redirect_url = reverse('inventory:type:index')
	return HttpResponseRedirect(redirect_url)


