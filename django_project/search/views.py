from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse


def test_view(request):
	"""
	A simple view for testing the search app interface.
	"""
	if not request.user.is_staff:
		raise Http404
	
	template = 'search/test.html'
	context = {}
	
	return render(request, template, context)


