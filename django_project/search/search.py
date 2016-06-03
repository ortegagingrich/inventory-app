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
		self, search_model, field_sources,
		max_display_items = 50,
		static_fields=None,
		result_template=None,
		result_header=None,
		result_header_template=None,
		no_match_template=None,
		object_label='object',
		context=None,
	):
		if len(field_sources) == 0:
			raise InvalidSearchSettings
		
		self.search_model = search_model
		
		self.result_template = result_template
		self.result_header = result_header
		self.result_header_template = result_header_template
		self.no_match_template = no_match_template
		
		
		self.object_label = object_label
		self.context = context
		
		# a dictionary whose keys are the attribute names of the models to be
		# searched and whose values will be replaced with the parsed values from
		# the input fields
		self.fields = {}
		for field in field_sources.keys():
			self.fields[field] = None
		
		# a dictionary whose keys are the attribute names of the models to be
		# searched and whose values are the names of the html input element to
		# be used to obtain the value
		self.field_sources = field_sources
		
		# static fields are for searches where there are fixed values at the
		# beginning.  For example, a search might be restricted to only items
		# belonging to a certain user. (e.g. static_fields = {'user': user})
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


