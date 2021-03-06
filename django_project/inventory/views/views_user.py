from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

from inventory.user.operations import *
import inventory.exceptions


#login

def login_page(request, error_message=None, redirect_url = None):
	if redirect_url == None:
		try:
			redirect_url = request.META.get('HTTP_REFERER')
		except:
			redirect_url = reverse('inventory:inventory_greeter')
	
	template = 'inventory/login_form.html'
	context = {
		'error_message': error_message,
		'redirect_url': redirect_url,
	}
	return render(request, template, context)


def login_submit(request):
	try:
		redirect_url = request.POST['redirecturl']
	except:
		redirect_url = None
	
	try:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
	except:
		#login somehow failed
		return login_page(request, 'Invalid Login.', redirect_url)
	
	if user != None:
		if user.is_active:
			login(request, user)
			if redirect_url != None:
				return HttpResponseRedirect(redirect_url)
			else:
				return HttpResponseRedirect(reverse('inventory:inventory_greeter'))
		else:
			error_message = 'Account Inactive.'
	else:
		error_message = 'Invalid Login.'
	return login_page(request, error_message, redirect_url)


def logout_submit(request):
	logout(request)
	return HttpResponseRedirect(reverse('inventory:inventory_greeter'))


#Profile operations


def signup_page(request, error_messages=None):
	template = 'inventory/signup_form.html'
	context = {
		'error_messages': error_messages,
	}
	return render(request, template, context)


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
		return profile_page(request, error_messages)
	
	try:
		update_user(user=request.user, email=email, fname=fname, lname=lname)
	except inventory.exceptions.InvalidValueError as error:
		message = error.message
		return profile_page(request, [message])
	except:
		raise Http404
	
	return profile_page(request)


def password_modify(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('inventory:inventory_greeter'))
	template = 'inventory/password_modify.html'
	context = {}
	return render(request, template, context)


#Change Password
def password_submit(request):
	from django.contrib.auth import update_session_auth_hash
	
	error_messages = []
	
	tentative_password = request.POST['password']
	repeat = request.POST['password_repeat']
	
	if tentative_password != repeat:
		error_messages.append('Entered Passwords do not match.')
	
	
	try:
		change_password(request.user, tentative_password)
		update_session_auth_hash(request, request.user)
	except inventory.exceptions.InvalidPasswordError as error:
		message = error.message
		error_messages.append(message)
	
	
	if len(error_messages) == 0:
		error_messages = ['Password Successfully Reset.']
	
	#Redirect to the profile page
	return profile_page(request, error_messages=error_messages)


#password reset views

def password_reset(request, error_messages=None):
	if error_messages != None:
		if len(error_messages) == 0:
			error_messages = None
	
	template = 'inventory/password_reset_form.html'
	context = {
		'error_messages': error_messages,
	}
	
	return render(request, template, context)


def password_reset_submit(request):
	error_messages = []
	print request.POST
	try:
		email = request.POST['email']
	except:
		message = 'Please enter a valid email address.'
		error_messages.append(message)
	
	if len(error_messages) > 0:
		return password_reset(request, error_messages)
	
	
	#get users matching the email address and send them reset emails
	users = User.objects.filter(email=email)
	for user in users:
		reset_password(user)
	
	
	template = 'inventory/password_reset_submit.html'
	context = {
		'email': email,
	}
	
	return render(request, template, context)


def signup_submit(request):
	
	#in case of failure
	def fail(messages):
		return signup_page(request, error_messages=messages)
	
	try:
		username = request.POST['username']
		email = request.POST['email']
	except:
		return fail(['Please enter a valid username and email address.'])
	
	
	#Attempt to create the account
	try:
		user, success, temp = create_user(
			username=username,
			email=email,
			fname='[FIRST NAME]',
			lname='[LAST NAME]',
		)
	except inventory.exceptions.InvalidValueError as error:
		message = error.message
		return fail([message])
	except inventory.exceptions.UserCreateError:
		message = 'Could not create user.'
		return fail([message])
	
	#Display Success Page
	if success:
		template = 'inventory/signup_success.html'
		context = {
			'username': user.username,
			'email': user.email,
		}
		return render(request, template, context)
	else: # Almost successful, but email did not work
		template = 'inventory/signup_no_email.html'
		context = {
			'username': user.username,
			'temporary_password': temp,
		}


