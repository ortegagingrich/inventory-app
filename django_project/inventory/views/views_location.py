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
def detail_page(request, location_key):
	location = get_object_or_404(Location, pk=location_key)
	
	if location.user != request.user and not request.user.is_staff:
		raise Http404
	
	template = 'inventory/location/detail.html'
	context = {
		'location': location,
		'item_list': Item.objects.filter(location=location),
	}
	return render(request, template, context)

