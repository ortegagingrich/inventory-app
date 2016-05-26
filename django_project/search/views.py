from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse

from .models import DictionaryEntry
from .search import SearchSettings


def test_view(request):
	"""
	A simple view for testing the search app interface.
	"""
	if not request.user.is_staff:
		raise Http404
	
	
	search_fields = ['word',]
	
	search_settings = SearchSettings(
		search_model=DictionaryEntry,
		field_names=search_fields,
	)
	
	
	template = 'search/test.html'
	context = {
		'search_settings': search_settings,
		'result_template': 'search/test_result.html',
		'object_label': 'entry',
	}
	
	return render(request, template, context)


