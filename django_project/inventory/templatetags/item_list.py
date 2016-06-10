from django import template


register = template.Library()

@register.inclusion_tag('inventory/item_list.html')
def item_list(items):
	"""
	A template tag to include a list of the provided items
	"""
	context = {
		'item_list': items,
	}
	
	return context
