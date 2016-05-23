from __future__ import unicode_literals

from datetime import date

from django.contrib.auth.models import User
from django.db import models


# Database model for individual notifications.
# These contain a string of characters to be substituted into an HTML file to
# display the notification.  For example, insert_text might be something like:
# '{% include inventory/error1.html %}'
class NotificationModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	id_string = models.CharField(max_length=20, default='') #string for id of the notification
	
	post_date = models.DateField()
	unread = models.BooleanField(default=True)
	
	insert_text = models.CharField(max_length=500)
	
	
	def __str__(self):
		string = '{} :{}<br /> {}'.format(
			self.post_date,
			self.name,
			self.insert_text
		)
		return string



def add_notification_link(user, name, message, url, id_string=None):
	"""
	Creates a notification which is displayed as a link to the provided url.
	"""
	if id_string == None:
		id_string = ''
	
	notification = NotificationModel(
		user=user,
		name=name,
		insert_text='<a href="{}">{}</a>'.format(url, message),
		id_string=id_string,
		post_date = date.today()
	)
	
	notification.save()
	return notification

