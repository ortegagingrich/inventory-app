"""
Basic Views for the Inventory System
"""

from django.http import HttpResponse
from django.shortcuts import render

def inventory_greeter(request):
	return HttpResponse("Welcome to the Inventory System")

def inventory_index(request):
	return HttpResponse("Inventory Index")


def item_detail(request, item_id = 42):
	return HttpResponse("Item: {}.".format(item_id))

def item_open(request, item_id):
	return HttpResponse("Opening item {}.".format(item_id))


def __test__():
	print "views test"
