from django import template


register = template.Library()

@register.inclusion_tag('search/search_form.html')
def search_form(request, search_fields, instructions=None):
	"""
	This is a custom template tag which generates a search submit form.  The
	'search_fields' argument is a dictionary whose keys are strings containing
	the names of the text input elements and whose corresponding values are
	strings which will serve as labels applied to these input elements
	"""
	
	context = {
		'search_fields': search_fields,
		'submit_url': request.path,
		'cancel_url': request.META.get('HTTP_REFERER'),
		'instructions': instructions,
	}
	
	return context


