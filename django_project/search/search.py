"""
Functions and Classes related to the searching.  For now, the searching itself
is done through the Django ORM and is done at the database level only.
"""
from .exceptions import InvalidSearchSettings


class SearchSettings(object):
	"""
	Object to hold settings related to the search itself as well as how it is
	to be displayed
	"""
	
	def __init__(
		self, search_model, field_names,
		max_display_items = 50,
		field_display_names=None,
		static_fields=None,
		result_template=None,
		no_match_template=None,
		object_label='object',
		context=None,
	):
		if len(field_names) == 0:
			raise InvalidSearchSettings
		
		self.search_model = search_model
		
		self.result_template = result_template
		self.no_match_template = no_match_template
		self.object_label = object_label
		self.context = context
		
		# a dictionary containing search field names and results
		self.fields = {}
		self.field_display_names = {}
		for field in field_names:
			self.fields[field] = None
			try:
				self.field_display_names[field] = field_display_names[field]
			except KeyError:
				self.field_display_names[field] = field
		
		if static_fields != None:
			self.static_fields = static_fields
		else:
			self.static_fields = {}
		
		self.max_display_items = max_display_items

	
	def execute_search(self):
		"""
		Attempts to execute a search with the provided settings.  Returns a
		Django queryset containing all matches.
		"""
		
		search_args = {}
		for field_name, field_value in self.fields.iteritems():
			if field_value != None:
				argument_name = '{}__icontains'.format(field_name)
				search_args[argument_name] = field_value
		for field_name, field_value in self.static_fields.iteritems():
			if field_value != None:
				search_args[field_name] = field_value
		
		
		# only do the search if there is at least one non-empty input
		if len(search_args) > 0:
			results = self.search_model.objects.filter(**search_args)
		else:
			results = self.search_model.objects.none()
		
		
		if len(results) > self.max_display_items:
			results = results[0:self.max_display_items - 1]
		
		return results


