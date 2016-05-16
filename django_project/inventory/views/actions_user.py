from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

from inventory.user.operations import create_user, update_user, change_password
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
	error_messages = []
	
	try:
		email = request.POST['email']
		fname = request.POST['first_name']
		lname = request.POST['last_name']
	except:
		message = 'Invalid Changes.'
		error_messages.append(message)
	
	
	if len(error_messages) > 0:
		return views.profile_page(request, error_messages)
	
	try:
		update_user(user=request.user, email=email, fname=fname, lname=lname)
	except ValidationError:
		message = 'Please enter a valid email address'
		return views.profile_page(request, [message])
	except:
		raise Http404
	
	return views.profile_page(request)


#Change Password
def password_change(request):
	error_messages = []
	
	tentative_password = request.POST['password']
	repeat = request.POST['password_repeat']
	
	if tentative_password != repeat:
		error_messages.append('Entered Passwords do not match.')
	
	
	error_messages += change_password(request.user, tentative_password)
	
	
	if len(error_messages) == 0:
		error_messages = ['Password Successfully Reset.']
	
	#Redirect to the profile page
	return views.profile_page(request, error_messages=error_messages)


#signup
def signup_submit(request):
	
	#in case of failure
	def fail(messages):
		return views.signup_page(request, error_messages=messages)
	
	try:
		username = request.POST['username']
		email = request.POST['email']
	except:
		return fail(['Please enter a valid username and email address.'])
	
	#Attempt to create the account
	(user, error_messages) = create_user(
		username=username,
		email=email,
		fname='[FIRST NAME]'
		lname='[LAST NAME]'
	)
	
	if user == None:
		return fail(error_messages)
	
	
	#Display Success Page
	template = 'inventory/signup_success.html'
	context = {
		'username': user.username,
		'temporary_password': temporary_password,
		'error_messages': error_messages,
	}
	return render(request, template, context)

