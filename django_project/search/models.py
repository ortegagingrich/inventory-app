from __future__ import unicode_literals

from django.db import models


# The models below are for testing purposes only.

MAX_DEF_LENGTH = 500
class DictionaryEntry(models.Model):
	word = models.CharField(max_length = 35)
	definition = models.CharField(max_length = MAX_DEF_LENGTH)
	
	def __str__(self):
		return self.word

class DuplicateEntry(models.Model):
	wordkey = models.CharField(max_length = 35)
	defval = models.CharField(max_length = MAX_DEF_LENGTH + 100)



def refresh_database():
	"""
	Deletes the current database entries and reloads them from file
	"""
	#first clear the existing database
	DictionaryEntry.objects.all().delete()
	DuplicateEntry.objects.all().delete()
	
	print('Database purged.')
	
	from testdata.load_data import load_dictionary_data
	data_dictionary = load_dictionary_data()
	
	new_data = []
	new_duplicates = []
	for word, definition in data_dictionary.iteritems():
		if(len(definition) <= MAX_DEF_LENGTH):
			new_data.append(DictionaryEntry(word=word, definition=definition))
			defval = 'Confucius say: ' + definition
			new_duplicates.append(DuplicateEntry(wordkey=word, defval=defval))
	
	print('Starting Bulk Create')
	DictionaryEntry.objects.bulk_create(new_data)
	DuplicateEntry.objects.bulk_create(new_duplicates)
	print('Finished Bulk Create')
			
	
	
