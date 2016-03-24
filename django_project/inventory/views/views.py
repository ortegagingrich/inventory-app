"""
Basic Views for the Inventory System
"""

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from inventory.models import *


#front page
def inventory_greeter(request):
	template = 'inventory/inventory_greeter.html'
	context = {}
	return render(request, template, context)

def inventory_index(request):
	items = Item.objects.order_by('printed_expiration_date')
	template = 'inventory/inventory_index.html'
	context = {
		'item_list': items,
	}
	return render(request, template, context)


def item_detail(request, item_id):
	template = 'inventory/item_detail.html'
	item = get_object_or_404(Item, pk=item_id)
	context = {
		'item': item,
	}
	return render(request, template, context)


def item_open(request, item_id):
	return HttpResponse("Opening item {}.".format(item_id))


def __test__():
	print "views test"
