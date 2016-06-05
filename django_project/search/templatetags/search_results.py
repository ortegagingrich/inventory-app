from django import template
from django.template.loader import render_to_string


register = template.Library()

@register.inclusion_tag('search/search_results.html')
def search_results(request, *search_settings_objects):
	"""
	This is a custom template tag created to allow the easy insertion of (very)
	basic database searching user-interfaces in my django apps.
	
	Note that this tag only inserts a results box.  The user must either make
	their own search query form or use the template tag {% search_query %} to
	make one.
	
	The {% search_results %} template tag must be given the current request as well
	as at least one SearchSettings object, which specifies the parameters of
	the search as well as the display settings of the results.
	
	Please see 'search.views.test_view' and its corresponding template
	'../search/templates/search/test.html' for an example of the proper usage
	of this template tag.
	"""
	
	# If no request has been made, (i.e. the page is loaded for the first tiem)
	# show no results
	if len(request.POST) == 0:
		rendered_results_list = None
	else: # A query is being made
		rendered_results_list = []
		
		#Conduct search and render each settings object
		for search_settings in search_settings_objects:
			results = _process_settings_object(request, search_settings)
			rendered_results_list += results
	
	
	context = {
		'rendered_results_list': rendered_results_list,
	}
	
	return context


def _process_settings_object(request, search_settings):
	"""
	Parses inputs from the request, conducts the search and returns a list of
	rendered results specific to the provided SearchSettings object
	"""
	# First, parse the search fields.
	for field_name, source in search_settings.field_sources.iteritems():
		search_words = request.POST[source].split()
		if len(search_words) > 0:
			search_settings.fields[field_name] = search_words
	
	# Do the actual search.
	search_results = search_settings.execute_search()
	
	# Now, produce the rendered results list
	rendered_results_list = [
		_render_result(result, search_settings) for result in search_results
	]
	
	# If, after everything, there are no results, either render the provided
	# template or provide a generic "No Results" message.
	if len(rendered_results_list) == 0:
		if search_settings.no_match_template != None:
			template = search_settings.no_match_template
			rendered_results_list = [render_to_string(template, {})]
		else:
			rendered_results_list = ['<font color="red">No Results</font>']
	
	# Header text or template
	if search_settings.result_header_template != None:
		template = search_settings.result_header_template
		rendered_results_list.insert(0, render_to_string(template, {}))
	elif search_settings.result_header != None:
		header_text = '<h2>{}</h2>'.format(search_settings.result_header)
		rendered_results_list.insert(0, header_text)
	
	return rendered_results_list


def _render_result(result_object, search_settings):
	"""
	Loads and renders the provided template with a context including the provided
	object with the provided label.  Returns a string containing the rendered
	html result.
	"""
	template = search_settings.result_template
	object_label = search_settings.object_label
	context = search_settings.context
	
	if template == None:
		return '<font color="blue">{}</font>'.format(result_object)
	
	if context == None:
		context = {}
	context[object_label] = result_object
	
	return render_to_string(template, context)


