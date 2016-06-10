from django import template
from django.core.urlresolvers import reverse

from django_project import settings


register = template.Library()

@register.simple_tag
def url_abs(name, *args):
	"""
	Basically identical to the built-in url tag, but includes the domain name
	"""
	protocol = settings.PROTOCOL
	domain = settings.DOMAIN
	url = reverse(name, args=args)
	abs_path = '{}://{}{}'.format(protocol, domain, url)
	
	return abs_path


