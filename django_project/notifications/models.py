from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Database model for individual notifications.
# These contain a string of characters to be substituted into an HTML file to
# display the notification.  For example, insert_text might be something like:
# '{% include inventory/error1.html %}'
class NotificationModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	insert_text = models.CharField(max_length=500)
	unread = models.BooleanField(default=True)


