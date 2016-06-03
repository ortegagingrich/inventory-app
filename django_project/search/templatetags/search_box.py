from django import template
from django.template.loader import render_to_string


register = template.Library()

@register.inclusion_tag('search/search_box.html')
def search_box(request, search_settings):
	#TODO: Add Docstring
	
	# If no request has been made, (i.e. the page is loaded for the first tiem)
	# show no results
	if len(request.POST) == 0:
		rendered_results_list = None
	else: # A query is being made, so parse the input fields
		# fill in search fields
		for field_name, source in search_settings.field_sources.iteritems():
			val = request.POST[source]
			if len(val) > 0:
				search_settings.fields[field_name] = val
		
		#execute the actual search
		results_list = search_settings.execute_search()
		
		rendered_results_list = [
			_render_result(result, search_settings) for result in results_list
		]
		
		#no results
		if len(rendered_results_list) == 0:
			if search_settings.no_match_template != None:
				template = search_settings.no_match_template
				rendered_results_list = [render_to_string(template, {})]
			else:
				rendered_results_list = ['<font color="red">No Results</font>']
		
		# insert header text or templates
		if search_settings.result_header_template != None:
			template = search_settings.result_header_template
			rendered_results_list.insert(0, render_to_string(template, {}))
		elif search_settings.result_header != None:
			header_text = '<h2>{}</h2>'.format(search_settings.result_header)
			rendered_results_list.insert(0, header_text)
	
	
	context = {
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


