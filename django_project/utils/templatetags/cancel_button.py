from django import template
from django.core.urlresolvers import reverse


register = template.Library()

@register.inclusion_tag('utils/cancel_button.html')
def cancel_button(request, default_url_name, *args, **kwargs):
	"""
	This template tag inserts a cancel button which, if possible, returns the
	user to the previous page when submitted.  If not, the user is redirected
	to the url with the provided name and arguments.
	"""
	
	cancel_url = request.META.get('HTTP_REFERER')
	if cancel_url == None:
		cancel_url = reverse(default_url_name, args=args, kwargs=kwargs)
		referer = 'None'
	else:
		referer = cancel_url
	
	context = {
		'referer': referer,
		'cancel_url': cancel_url,
	}
	
	return context


