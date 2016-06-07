"""
Contains functions which are triggered by certain signals/events
"""
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

from inventory.models import Item, UserProfile


@receiver(user_logged_in)
def on_login(sender, user, **kwargs):
	"""
	Executed when a user has just logged in
	"""
	
	#update notifications pertaining to items
	Item.update_notifications(user)



@receiver(models.signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.on_require_reset(user=instance)


@receiver(models.signals.pre_save, sender=User)
def update_profile(sender, instance, **kwargs):
	if instance:
		new_password = instance.password
		try:
			old_password = User.objects.get(pk=instance.pk).password
		except User.DoesNotExist:
			#This means that the user is just being created; still needs password reset
			return
		
		if new_password != old_password:
			UserProfile.on_reset(user=instance)

