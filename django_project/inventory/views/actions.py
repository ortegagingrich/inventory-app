from datetime import date

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

from inventory.models import *


def item_open(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	
	if not 'choice' in request.POST.keys():
		print "No Choice"
		return HttpResponseRedirect(reverse("inventory:item_detail", args=(item_id)))
	
	if request.POST['choice'] == "today":
		open_date = date.today()
	elif request.POST['choice'] == "other":
		other_date = request.POST['open_date']
		print other_date
		if other_date == '':
			return HttpResponseRedirect(reverse("inventory:item_detail", args=(item_id)))
		open_date = other_date
	else:
		return HttpResponseRedirect(reverse("inventory:item_detail", args=(item_id)))
	
	if not item.opened:
		item.opened_date = open_date
		item.save()
	
	#return HttpResponse("Opening item {}.".format(item_id))
	#return item_detail(request, item_id)
	return HttpResponseRedirect(reverse("inventory:item_detail", args=(item_id)))
