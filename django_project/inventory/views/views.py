"""
Basic Views for the Inventory System
"""
from datetime import date

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core.urlresolvers import reverse

from inventory.models import *


#front page
def inventory_greeter(request):
	template = 'inventory/inventory_greeter.html'
	context = {}
	return render(request, template, context)


#login page
def login_page(request, error_message=None):
	template = 'inventory/login_form.html'
	context = {
		'error_message': error_message,
	}
	return render(request, template, context)

def signup_page(request, error_message=None):
	template = 'inventory/signup_form.html'
	context = {
		'error_message': error_message,
	}
	return render(request, template, context)

#account profile
def profile_page(request, error_messages=None):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('inventory:inventory_greeter'))
	template = 'inventory/profile.html'
	context = {
		'error_messages': error_messages,
	}
	return render(request, template, context)

def profile_modify(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('inventory:inventory_greeter'))
	template = 'inventory/profile_modify.html'
	context = {}
	return render(request, template, context)

#Views for Inventory objects

class IndexView(generic.ListView):
	template_name = 'inventory/inventory_index.html'
	context_object_name = 'item_list' #name used in the template
	
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return super(IndexView, self).dispatch(request, *args, **kwargs)
		else:
			return HttpResponseRedirect(reverse('inventory:inventory_greeter'))
	
	def get_queryset(self):
		if self.request.user.is_staff:
			itemset = Item.objects.order_by('printed_expiration_date')
			return itemset.order_by('user')
		else:
			itemset = Item.objects.filter(user=self.request.user)
			return itemset.order_by('printed_expiration_date')


class ItemDetailView(generic.DetailView):
	model = Item
	template_name = 'inventory/item_detail.html'
	
	def dispatch(self, request, *args, **kwargs):
		owner = Item.objects.get(pk=kwargs['pk']).user
		if request.user != owner and not request.user.is_staff:
			raise Http404
		return super(ItemDetailView, self).dispatch(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super(ItemDetailView, self).get_context_data(**kwargs)
		#print context
		return context


class ItemOpenView(ItemDetailView):
	template_name = 'inventory/item_open.html'

def __test__():
	print "views test"
