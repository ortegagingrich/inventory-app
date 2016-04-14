"""
Views and Actions for cruding location models
"""

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core.urlresolvers import reverse

from inventory.models import *


#Index view
class IndexView(generic.ListView):
	template_name = 'inventory/location/index.html'
	context_object_name = 'location_list'
	
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return super(IndexView, self).dispatch(request, *args, **kwargs)
		else:
			return HttpResponseRedirect(reverse('inventory:inventory_greeter'))
	
	def get_queryset(self):
		return Location.objects.filter(user=self.request.user)


#detail view
def detail_page(request, location_key, error_messages=None):
	location = get_object_or_404(Location, pk=location_key)
	
	if location.user != request.user and not request.user.is_staff:
		raise Http404
	
	if error_messages != None:
		if len(error_messages) == 0:
			error_messages = None
	
	template = 'inventory/location/detail.html'
	context = {
		'location': location,
		'item_list': Item.objects.filter(location=location),
		'error_messages': error_messages
	}
	return render(request, template, context)


#rename
def rename_submit(request, location_key):
	location = get_object_or_404(Location, pk=location_key)
	
	if location.user != request.user and not request.is_staff:
		raise Http404
	
	error_messages = []
	
	try:
		new_name = request.POST['rename']
		
		if len(new_name) < 1:
			message = 'Cannot rename location "{}" to "{}".  '
			message += 'Location names must have at least one character.'
			error_messages.append(message.format(location.name, new_name))
		elif '\'' in new_name or '\"' in new_name:
			message = "Names cannot contain apostrophes or quotations."
			error_messages.append(message)
		else:
			location.name = new_name
			location.save()
	except:
		error_messages.append('Please enter a valid name.')
	
	return detail_page(request, location_key, error_messages)


