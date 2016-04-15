"""
Views and Actions for cruding ItemType models
"""

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core.urlresolvers import reverse

from inventory.models import *


#Index view
class IndexView(generic.ListView):
	template_name = 'inventory/type/index.html'
	context_object_name = 'type_list'
	
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return super(IndexView, self).dispatch(request, *args, **kwargs)
		else:
			return HttpResponseRedirect(reverse('inventory:inventory_greeter'))
	
	def get_queryset(self):
		return ItemType.objects.filter(user=self.request.user, open_grocery_entry=None)
