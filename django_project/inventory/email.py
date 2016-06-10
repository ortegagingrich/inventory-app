"""
Contains routines for sending emails to users.
"""
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from django_project import settings

import inventory.exceptions


DOMAIN = settings.DOMAIN
FROM_EMAIL = 'ortegagingrich@gmail.com'


def send_expiration_report(user, new_expired, old_expired=None, 
                           new_warning=None, old_warning=None):
	"""
	If appropriate, sends an email to the provided user indicating recently
	expired or soon to expire items.
	"""
	if new_warning == None:
		new_warning = []
	if old_warning == None:
		old_warning = []
	if old_expired == None:
		old_expired = []
	
	# If no recently expired items, do nothing
	if max(len(new_expired), len(new_warning)) == 0:
		return
	
	# list of all items that will soon expire
	warning = new_warning + old_warning
	context = {
		'user': user,
		'new_expired': new_expired,
		'old_expired': old_expired,
		'warning': warning,
	}
	template = 'inventory/email/expiration_report.html'
	
	
	subject = 'Inventory Expiration Report'
	message = render_to_string(template, context)
	
	if not settings.DEBUG:
		email = user.email
	else:
		email = FROM_EMAIL
	
	mail = EmailMessage(subject, message, FROM_EMAIL, [email])
	mail.content_subtype = 'html'
	
	mail.send()


def send_temporary_password(user, temporary_password):
	"""
	Sends an email to the provided user with the provided temporary password.
	"""
	login_url = DOMAIN + reverse('inventory:inventory_greeter')
	
	subject = 'Account Password Reset'
	
	message = """<!DOCTYPE html>
	<html>
		<body>
			Hello {}
			<br /> <br />
			Welcome to the inventory system.<br />
			Your temporary password is: <font color=blue>{}</font><br /><br />
			Please login
			<a href="{}">here</a>
			and change your password as soon as possible.
			
			
			
			Inventory System
		</body>
	</html>
	""".format(user.username, temporary_password, login_url)
	
	#only send to the user's actual email if not in debug mode
	if not settings.DEBUG:
		email = user.email
	else:
		email = FROM_EMAIL
	
	mail = EmailMessage(subject, message, FROM_EMAIL, [email])
	mail.content_subtype = 'html'
	
	try:
		mail.send()
	except Exception as ex:
		raise inventory.exceptions.InvalidEmailError(user.email)
	

