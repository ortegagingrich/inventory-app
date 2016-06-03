from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse

from .models import DictionaryEntry, DuplicateEntry
from .search import SearchSettings


def test_view(request):
	"""
	A simple view for testing the search app interface.
	"""
	if not request.user.is_staff:
		raise Http404
	
	
	search_fields = {
		'word': 'word_element',
	}
	
	search_settings_1 = SearchSettings(
		search_model=DictionaryEntry,
		field_sources=search_fields,
		result_template='search/test_result_1.html',
		result_header='According to Professor Webster:',
		object_label='entry',
	)
	
	
	search_fields = {
		'wordkey': 'word_element',
	}
	
	search_settings_2 = SearchSettings(
		search_model=DuplicateEntry,
		field_sources=search_fields,
		result_header='Ancient Wisdom:',
		result_template='search/test_result_2.html',
		object_label='entry'
	)
	
	
	
	display_names = {'word_element': 'Word'}
	
	template = 'search/test.html'
	context = {
		'search_settings_1': search_settings_1,
		'search_settings_2': search_settings_2,
		'submit_url': request.path,
		'search_fields': display_names,
	}
	
	return render(request, template, context)


