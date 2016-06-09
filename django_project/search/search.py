"""
Functions and Classes related to the searching.  For now, the searching itself
is done through the Django ORM and is done at the database level only.
"""
from django.db.models.functions import Length

from .exceptions import InvalidSearchSettings


class SearchSettings(object):
	"""
	Object to hold settings related to the search itself as well as how it is
	to be displayed
	"""
	
	def __init__(
		self, search_model,
		field_sources=None,
		sort_by_length_fields=None, # A list of field_names to sort by length
		max_display_items=50,
		static_fields=None,
		result_template=None,
		result_header=None,
		result_header_template=None,
		no_match_template=None,
		object_label='object',
		context=None,
	):
		if field_sources == None:
			field_sources = {}
		
		self.search_model = search_model
		
		self.result_template = result_template
		self.result_header = result_header
		self.result_header_template = result_header_template
		self.no_match_template = no_match_template
		
		
		self.object_label = object_label
		self.context = context
		
		# a dictionary whose keys are the attribute names of the models to be
		# searched and whose values will be replaced with a list of the parsed
		# values from the input fields (split, of course, by whitespace)
		self.fields = {}
		for field in field_sources.keys():
			self.fields[field] = None
		
		if sort_by_length_fields != None:
			# check to make sure these are valid fields
			for name in sort_by_length_fields:
				if not name in self.fields.keys():
					raise InvalidSearchSettings
			self.sort_by_length_fields = sort_by_length_fields
		else:
			self.sort_by_length_fields = self.fields.keys()
		
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
		
		# Since searching multiple words under the same field is allowed and
		# each application of the django filter function to a queryset only
		# allows one input per field (i.e. we can only search to see if a 
		# column contains a single word at a time), we will have to apply the
		# filter function iteratively.  The example below illustrates the scheme:
		# 
		# Suppose that we are conducting a search for objects whose field_1 string
		# contains both 'foo' and 'bar' and whose field_2 string contains 'baz'.
		# 
		# We must apply the filter function twice to search field_1 for two
		# substrings.  Thus, we build a list of kwargs dictionaries as follows:
		# 
		# [{'field_1': 'foo', 'field_2': 'baz'}, {'field_1': 'bar'}]
		# 
		# See the code below for the details.  This explanation is just to
		# try to illuminate why the code is this way.
		
		#determine how many times the filter operator will have to be applied
		filter_iterations = self._count_filter_iterations()
		
		#create and fill in a list of dictionaries of the appropriate length
		search_args_list = [{} for i in range(0, filter_iterations)]
		for field_name, field_values in self.fields.iteritems():
			#skip fields which were left blank
			if field_values == None:
				continue
			
			argument_name = '{}__icontains'.format(field_name)
			
			entry_count = 0
			while entry_count < len(field_values):
				search_args = search_args_list[entry_count]
				search_args[argument_name] = field_values[entry_count]
				
				entry_count += 1
		
		static_search_args = {}
		for field_name, field_value in self.static_fields.iteritems():
			static_search_args[field_name] = field_value
		
		
		# only do the search if there is at least one non-empty input
		if len(search_args_list) == 0:
			results = self.search_model.objects.none()
		elif max(map(len, search_args_list)) == 0:
			results = self.search_model.objects.none()
		else:
			# Carry out the actual search
			# First, by filtering according to the static items
			results = self.search_model.objects.filter(**static_search_args)
			
			# Now, progressively apply filters from the entry fields
			for search_args in search_args_list:
				results = results.filter(**search_args)
		
		
		for field_name in self.sort_by_length_fields:
			try:
				mod_results = results.annotate(text_len=Length(field_name))
				mod_results = mod_results.order_by('text_len')
				results = mod_results
			except Exception as ex:
				pass
		
		
		if len(results) > self.max_display_items:
			results = results[0:self.max_display_items]
		
		return results
	
	
	def _count_filter_iterations(self):
		"""
		Determines how many times the filter operation will have to be applied
		in the sorting process.  Essentially, this is the length of the longest
		field value list.
		"""
		values = [val for val in self.fields.values() if val != None]
		if len(values) != 0:
			return max(map(len, values))
		else:
			return 0


