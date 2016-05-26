from functools import partial

from django import template
from django.template.loader import render_to_string


register = template.Library()

@register.inclusion_tag('search/search_box.html')
def search_box(request, search_settings):
	#TODO: Add Docstring
	
	# check to see if a search request has already been made
	try:
		for field_name in search_settings.fields.keys():
			val = request.POST[field_name]
			if len(val) > 0:
				search_settings.fields[field_name] = val
	except:
		# no search has been submitted yet, so no results
		rendered_results_list = None
	else:
		results_list = search_settings.execute_search()
		
		rendered_results_list = [
			_render_result(result, search_settings) for result in results_list
		]
		
		#no results
		if len(rendered_results_list) == 0:
			rendered_results_list = ['<font color="red">No Results</font>']
	
	context = {
		'search_fields': search_settings.field_display_names,
		'submit_url': request.path,
		'rendered_results_list': rendered_results_list,
	}
	
	return context


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


