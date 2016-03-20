"""
Basic Views for the Inventory System
"""

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
	return HttpResponse("Inventory Index")


def __test__():
	print "views test"
