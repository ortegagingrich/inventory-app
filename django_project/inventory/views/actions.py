from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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

#Profile modification
def profile_submit(request):
	
	#once all possible changes have been made
	def finish(messages):
		request.user.save()
		if len(messages) == 0:
			messages = None
		return views.profile_page(request, error_messages=messages)
	
	try:
		email = request.POST['email']
		fname = request.POST['first_name']
		lname = request.POST['last_name']
	except:
		return finish(['Invalid Changes.'])
	
	error_messages = []
	
	#check that the new email is valid
	from django.core.validators import validate_email
	from django.core.exceptions import ValidationError
	try:
		validate_email(email)
	except ValidationError:
		error_messages.append('Invalid Email Address "{}"'.format(email))
	else:
		request.user.email = email
	
	#set first and last names
	request.user.first_name = fname
	request.user.last_name = lname
	
	return finish(error_messages)
	

#signup
def signup_submit(request):
	
	#in case of failure
	def fail(message):
		return views.signup_page(request, error_message=message)
	
	try:
		username = request.POST['username']
		email = request.POST['email']
	except:
		return fail('Please enter a valid username and email address.')
	
	#First, check that the "email" is actually a valid address
	from django.core.validators import validate_email
	from django.core.exceptions import ValidationError
	try:
		validate_email(email)
	except ValidationError:
		return fail('Please enter a valid email address.')
	
	#Next, check to make sure that the username is alright
	if len(username) < 5:
		return fail('Please enter a username with at least five characters.')
	if User.objects.filter(username=username).exists():
		message = 'The username "{}" is already taken.  Please choose another.'
		return fail(message.format(username))
	
	#TODO: better automatic password
	temporary_password = 'password'
	try:
		user = User.objects.create_user(username, email, temporary_password)
	except:
		return fail('Could not create account.  Please try again.')
	
	
	#Signup success
	template = 'inventory/signup_success.html'
	context = {
		'username': user.username,
		'temporary_password': user.password,
	}
	return render(request, template, context)


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
