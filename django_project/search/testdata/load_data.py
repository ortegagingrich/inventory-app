import json
from os.path import join, abspath, dirname


INPUT_FILE = join(dirname(abspath(__file__)), 'dictionary', 'dictionary.json')

def load_dictionary_data():
	
	with open(INPUT_FILE) as input_file:
		raw_data = input_file.read()
		dictionary = json.loads(raw_data)
	
	return dictionary


if __name__ == '__main__':
	load_dictionary_data()

