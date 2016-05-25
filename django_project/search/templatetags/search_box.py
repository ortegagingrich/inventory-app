from django import template


register = template.Library()

@register.inclusion_tag('search/search_box.html')
def search_box(request):
	
	search_fields = [
		'Name',
	]
	
	
	# check to see if a search request has already been made
	try:
		field_submissions = dict([ 
			(fieldname, request.POST[fieldname]) for fieldname in search_fields 
		])
		#TODO: do the actual search here
		results_list = [
			'<font color="blue">{}</font>'.format(v) 
			for v in field_submissions.values()
		]
	except:
		#No search yet, so no results
		results_list = None
	
	
	context = {
		'search_fields': search_fields,
		'submit_url': request.path,
		'results_list': results_list,
	}
	
	return context

