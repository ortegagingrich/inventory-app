"""
Views and Actions for cruding location models
"""

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core.urlresolvers import reverse

from inventory.models import *
from inventory.location.operations import *
from inventory.views import views_user
import inventory.exceptions


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


def detail_page(request, location_key, error_messages=None):
	if not request.user.is_authenticated():
		redirect_url = request.get_full_path()
		return views_user.login_page(request, redirect_url=redirect_url)
		
	
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



def create_submit(request):
	if not request.user.is_authenticated():
		raise Http404
	
	error_messages = []
	
	try:
		name = request.POST['name']
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
	
	try:
		location = create_location(
			user=request.user,
			name=name,
			refrigerated=refrigerated,
			frozen=frozen,
		)
	except inventory.exceptions.InvalidValueError as error:
		message = error.message
		error_messages.append(message)
	except:
		message = 'Could not create location.'
		error_messages.append(message)
	
	
	if len(error_messages) > 0:
		return create_page(request, error_messages)
	
	redirect_url = reverse('inventory:location:detail', args=(location.id,))
	return HttpResponseRedirect(redirect_url)



def rename_submit(request, location_key):
	error_messages = []
	
	try:
		name = request.POST['rename']
	except:
		error_messages.append('Please enter a valid name.')
	
	try:
		rename_location(request.user, location_key, name)
	except inventory.exceptions.InvalidLocationError:
		raise Http404
	except inventory.exceptions.InvalidValueError as error:
		message = error.message
		error_messages.append(message)
	except:
		message = 'Could not rename the location.'
		error_messages.append(message)
	
	
	if len(error_messages) > 0:
		return detail_page(request, location_key, error_messages)
	
	redirect_url = reverse('inventory:location:detail', args=(location_key,))
	return HttpResponseRedirect(redirect_url)



def delete_submit(request, location_key):
	try:
		delete_location(request.user, location_key)
	except:
		raise Http404
	
	redirect_url = reverse('inventory:location:index')
	return HttpResponseRedirect(redirect_url)


