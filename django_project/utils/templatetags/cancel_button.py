from django import template


register = template.Library()

@register.inclusion_tag('utils/cancel_button.html')
def cancel_button(request, default_url_name, *args, **kwargs):
	"""
	This template tag inserts a cancel button which, if possible, returns the
	user to the previous page when submitted.  If not, the user is redirected
	to the url with the provided name and arguments.
	"""
	context = {}
	
	return context


