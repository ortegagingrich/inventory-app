from django import template

from notifications.models import NotificationModel

register = template.Library()


@register.inclusion_tag('notifications/notification_bar.html')
def notification_bar(user, notification_url=None):
	"""
	Template Tag to produce a notification bar for the provided user.
	"""
	notifications = NotificationModel.objects.filter(user=user)
	
	context = {
		'notification_count': len(notifications),
		'notification_url': notification_url,
	}
	return context

