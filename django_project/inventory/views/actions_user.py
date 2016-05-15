from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

from inventory.models import *
from inventory.user import defaults
from inventory.views import views

#TODO: NEEDS REFACTOR
#TODO: All functionality herein not directly related to form entries should be
#      moved elsewhere.

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
	
	# function to be run once the form has been read and all possible
	# changes have been made
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
	
	#TODO: BEGIN MOVE
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
	#TODO: END MOVE
	
	return finish(error_messages)


#Change Password
def password_change(request):
	error_messages = []
	
	tentative_password = request.POST['password']
	repeat = request.POST['password_repeat']
	
	if tentative_password != repeat:
		error_messages.append('Entered Passwords do not match.')
	
	
	#TODO: BEGIN MOVE
	if len(tentative_password) < 6:
		error_messages.append('Passwords must have at least 6 characters.')
	
	if len(error_messages) == 0:
		#change password
		request.user.set_password(tentative_password)
		request.user.save()
	#TODO: END MOVE
	
	
	if len(error_messages) == 0:
		error_messages = ['Password Successfully Reset.']
	
	#Redirect to the profile page
	return views.profile_page(request, error_messages=error_messages)


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
	
	#TODO: BEGIN MOVE
	
	#First, check that the "email" is actually a valid address
	from django.core.validators import validate_email
	from django.core.exceptions import ValidationError
	try:
		validate_email(email)
	except ValidationError:
		return fail('Please enter a valid email address.')
	
	if '\'' in username or '\"' in username:
		return fail('Usernames cannot contain quotations or apostrophes.')
	
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
	
	
	#Signup success; create default database
	defaults.create_user_defaults(user)
	
	#Display Success Page
	template = 'inventory/signup_success.html'
	context = {
		'username': user.username,
		'temporary_password': temporary_password,
	}
	return render(request, template, context)

