from datetime import timedelta

from django.contrib.auth.models import User

from celery.decorators import periodic_task
from celery.schedules import crontab

from inventory.models import Item
from inventory.email import send_expiration_report


@periodic_task(
	run_every=crontab(hour=0, minute=5),
	name='task_generate_daily_emails',
	ignore_result=True,
)
def _task_generate_daily_emails():
	"""
	A wrapper for celery around generate_daily_emails
	"""
	generate_daily_emails

def generate_daily_emails(user=None):
	"""
	Generates and sends all daily emails for the provided user.  If no user
	is provided, the emails are generated and sent for all active users.
	"""
	if user==None:
		userset = User.objects.filter(is_active=True)
		for u in userset:
			generate_daily_emails(u)
		return
	
	all_items = Item.objects.filter(user=user)
	
	new_expired = []
	old_expired = []
	new_warning = []
	old_warning = []
	for item in all_items:
		if item.expired:
			if item._email_expiration:
				old_expired.append(item)
			else:
				new_expired.append(item)
				item._email_expiration = True
				item.save()
		elif item.soon_to_expire:
			if item._email_old:
				old_warning.append(item)
			else:
				new_warning.append(item)
				item._email_old = True
				item.save()
	
	try:
		send_expiration_report(user, new_expired, old_expired, new_warning, old_warning)
	except Exception as ex:
		print('Daily expiration email to {} failed: {}'.format(user, ex))



@periodic_task(
	run_every=timedelta(seconds=60),
	name='task_update_user_notifications',
	ignore_result=True,
)
def _task_update_user_notifications():
	"""
	A wrapper for celery around update_user_notifications.
	"""
	update_user_notifications()

def update_user_notifications():
	"""
	Cycles through all active users and updates their notifications
	"""
	userset = User.objects.filter(is_active=True)
	
	for user in userset:
		Item.update_notifications(user)

