"""
Views and Actions for cruding location models
"""

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core.urlresolvers import reverse

from inventory.models import *

#TODO: NEEDS REFACTOR


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
		'error_messages': error_messages,
	}
	return render(request, template, context)


def create_page(request, error_messages=None):
	if error_messages != None:
		if len(error_messages) == 0:
			error_messages = None
	
	if not request.user.is_authenticated:
		raise Http404
	
	template = 'inventory/location/create.html'
	context = {
		'error_messages': error_messages
	}
	return render(request, template, context)


#Create
def create_submit(request):
	if not request.user.is_authenticated():
		raise Http404
	
	(location, error_messages) = create_location(request)
	
	if location == None:
		return create_page(request, error_messages)
	
	redirect_url = reverse('inventory:location:detail', args=(location.id,))
	return HttpResponseRedirect(redirect_url)


#TODO: functionality should really be somewhere else and independent of request
def create_location(request):
	"""
	Attempts to return a location using the given request.
	Returns a tuple containing the new location (or None, if unsuccessful) and
	a list of error messages
	"""
	error_messages = []
	
	try:
		name = request.POST['name']
		if len(name) < 1:
			message = 'Cannot name location "{}".  '
			message += 'Location names must have at least one character.'
			error_messages.append(message.format(name))
		elif '\'' in name or '\"' in name:
			message = "Names cannot contain apostrophes or quotations."
			error_messages.append(message)
	except:
		error_messages.append('Please enter a valid name')
	
	if not 'temperature' in request.POST.keys():
		error_messages.append('Could not create location.  No temperature was selected.')
	else:
		temp = request.POST['temperature']
		if temp == 'frozen':
			frozen = True
			refrigerated = False
		elif temp == 'refrigerated':
			frozen = False
			refrigerated = True
		elif temp == 'room_temperature':
			frozen = False
			refrigerated = False
		else:
			error_messages.append('Could not create location.  No temperature was selected.')
	
	if len(error_messages) > 0:
		location = None
	else:
		#finally, create and save location
		location = Location(user=request.user, name=name, frozen=frozen,
	              	        refrigerated = refrigerated)
		location.save()
	
	return (location, error_messages)


#rename
def rename_submit(request, location_key):
	location = get_object_or_404(Location, pk=location_key)
	
	if location.user != request.user and not request.user.is_staff:
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
	
	if len(error_messages) > 0:
		return detail_page(request, location_key, error_messages)
	else:
		redirect_url = reverse('inventory:location:detail', args=(location.id,))
		return HttpResponseRedirect(redirect_url)


def delete_submit(request, location_key):
	location = get_object_or_404(Location, pk=location_key)
	
	if request.user != location.user or not request.user.is_authenticated():
		raise Http404
	
	location.delete()
	
	redirect_url = reverse('inventory:location:index')
	return HttpResponseRedirect(redirect_url)


