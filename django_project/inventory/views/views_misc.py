"""
Basic Views for the Inventory System
"""
from django.shortcuts import render


#front page
def inventory_greeter(request):
	template = 'inventory/inventory_greeter.html'
	context = {}
	return render(request, template, context)


