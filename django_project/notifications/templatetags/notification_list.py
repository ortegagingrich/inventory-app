from django import template

from notifications.models import NotificationModel

register = template.Library()


@register.inclusion_tag('notifications/notification_list.html')
def notification_list(user):
	"""
	Template Tag to produce a detailed list of notifications for the provided user.
	"""
	notifications = NotificationModel.objects.filter(user=user)
	
	#set notifications as read
	for notification in notifications:
		notification.unread = False
		notification.save()
	
	context = {
		'notifications': notifications,
		'notification_count': len(notifications),
	}
	return context

