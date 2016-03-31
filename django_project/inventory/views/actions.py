from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

from inventory.models import *
from inventory.views import views


#login
def login_action(request):
	try:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
	except:
		#login somehow failed
		return views.login_page(request, "Invalid Login.")
	
	if user != None:
		if user.is_active:
			login(request, user)
			return HttpResponseRedirect(reverse("inventory:inventory_greeter"))
		else:
			error_message = "Account Inactive."
	else:
		error_message = "Invalid Login."
	return views.login_page(request, error_message)

def logout_action(request):
	logout(request)
	return HttpResponseRedirect(reverse("inventory:inventory_greeter"))

#signup
def signup_submit(request):
	#TODO:
	pass


def item_open(request, item_id):
	"""
	Action to assign an opening date to an item.
	"""
	item = get_object_or_404(Item, pk=item_id)
	
	#check that the user really has the authority to do this
	if item.user != request.user:
		raise Http404()
	
	#if the user did not select either "today" or a custom date for opening
	if not 'choice' in request.POST.keys():
		print "No Choice"
		return HttpResponseRedirect(reverse("inventory:item_detail", args=(item_id)))
	
	if request.POST['choice'] == "today":
		open_date = date.today()
	elif request.POST['choice'] == "other":
		other_date = request.POST['open_date']
		print other_date
		if other_date == '':
			return HttpResponseRedirect(reverse("inventory:item_detail", args=(item_id)))
		open_date = other_date
	else:
		return HttpResponseRedirect(reverse("inventory:item_detail", args=(item_id)))
	
	if not item.opened:
		item.opened_date = open_date
		item.save()
	
	#return HttpResponse("Opening item {}.".format(item_id))
	#return item_detail(request, item_id)
	return HttpResponseRedirect(reverse("inventory:item_detail", args=(item_id)))
