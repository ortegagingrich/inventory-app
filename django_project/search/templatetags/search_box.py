from django import template


register = template.Library()

@register.inclusion_tag('search/search_box.html')
def search_box(request, search_settings):
	
	
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
		
		
		#TODO: figure out results rendering
		rendered_results_list = map(_build_rendered_result, results_list)
	
	
	context = {
		'search_fields': search_settings.fields.keys(),
		'submit_url': request.path,
		'rendered_results_list': rendered_results_list,
	}
	
	return context


def _build_rendered_result(result_object):
	"""
	
	"""
	return '<font color="blue">{}</font>'.format(result_object)


