"""
Contains routines for sending emails to users.
"""
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse

import inventory.exceptions


DOMAIN = '127.0.0.1'
FROM_EMAIL = 'ortegagingrich@gmail.com'

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
	
	mail = EmailMessage(subject, message, FROM_EMAIL, [user.email])
	mail.content_subtype = 'html'
	
	try:
		mail.send()
	except Exception as ex:
		raise inventory.exceptions.InvalidEmailException(user.email)
	

