"""
Actions that are only available to staff users
"""

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render


def _verify_admin(request):
	user = request.user
	return user.is_staff and user.is_active and user.is_authenticated()


"""
Danger Zone!!!
"""

def purge_database(request):
	"""
	Be very careful with this one.  Purges all non-staff non-default database
	entries.
	"""
	from inventory.user.purge import purge_database_user
	
	user = request.user
	if not _verify_admin(request):
		raise Http404
	
	print('About to purge database.')
	
	purged_items = []
	
	for purge_user in User.objects.all():
		if not purge_user.is_staff:
			purged_items += purge_database_user(purge_user)
	
	
	context={
		'purged_items': purged_items,
	}
	template = 'inventory/admin/purge_database.html'
	return render(request, template, context)

