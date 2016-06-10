from datetime import timedelta

from django.contrib.auth.models import User

from celery.decorators import periodic_task

from inventory.models import Item




@periodic_task(
	run_every=timedelta(seconds=60),
	name='task_update_user_notifications',
	ignore_result=True,
)
def task_update_user_notifications():
	"""
	Cycles through all active users and updates their notifications
	"""
	userset = User.objects.filter(is_active=True)
	
	print 'Doing Stuff'
	
	for user in userset:
		Item.update_notifications(user)


