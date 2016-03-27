"""
Basic Views for the Inventory System
"""
from datetime import date

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from inventory.models import *


#front page
def inventory_greeter(request):
	template = 'inventory/inventory_greeter.html'
	context = {}
	return render(request, template, context)


class IndexView(generic.ListView):
	template_name = 'inventory/inventory_index.html'
	context_object_name = 'item_list' #name used in the template
	
	def get_queryset(self):
		return Item.objects.order_by('printed_expiration_date')


class ItemDetailView(generic.DetailView):
	model = Item
	template_name = 'inventory/item_detail.html'
	
	def get_context_data(self, **kwargs):
		context = super(ItemDetailView, self).get_context_data(**kwargs)
		print context
		return context


class ItemOpenView(generic.DetailView):
	model = Item
	template_name = 'inventory/item_open.html'

def __test__():
	print "views test"
