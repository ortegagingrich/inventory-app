"""
Contains functions which are triggered by certain signals/events
"""
from django.db import models
from django.dispatch import receiver

from inventory.models import Item

from notifications.models import NotificationModel


@receiver(models.signals.pre_delete, sender=Item)
def on_item_delete(sender, instance, **kwargs):
	#clear any unread notifications related to this item
	id_match = 'item_{}'.format(instance.id)
	notifications = NotificationModel.objects.filter(
		user=instance.user,
		id_string=id_match,
	)
	
	for notification in notifications:
		if notification.unread:
			notification.delete()


