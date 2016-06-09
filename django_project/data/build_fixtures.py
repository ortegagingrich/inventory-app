"""
Contains a brief script to parse the Grocery_UPC_Database.xlsx file available
from the Open Grocery Website and build a json file to be used as a database
fixture.  Note that the json file is kept in version control while the xlsx is
not.  If, for some reason, the json file needs to be built from scratch, the
xlsx file should be obtained from

http://www.grocery.com/open-grocery-database-project/

and placed inside the same directory as this script.  This script should then be
executed.

EDIT:
	Please convert the xlsx to csv first.
"""
import os


DATA_PATH = os.path.dirname(os.path.abspath(__file__))


def build_fixtures():
	"""
	Builds all fixtures necessary for this project
	"""
	try:
		build_fixtures_upc()
	except Exception as ex:
		print('Failed to build fixtures for UPC database.')
		print(ex)


def build_fixtures_upc():
	"""
	Builds fixtures for the upc database if the input file is found.  If there
	already exists a corresponding fixture, the user is prompted whether or not
	to overwrite the existing file.
	"""
	input_file_name = 'Grocery_UPC_Database.csv'
	input_file_path = os.path.join(DATA_PATH, input_file_name)
	
	with open(input_file_path) as input_file:
		data = input_file.read()
	
	#check to see if json file already exists
	output_file_name = 'grocery_upc_database.json'
	output_file_path = os.path.join(DATA_PATH, output_file_name)
	
	if os.path.exists(output_file_path):
		print('A UPC fixture file already exists.  Do you wish to overwrite it? [Y,n]')
		if raw_input() in ['Y']:
			os.remove(output_file_path)
		else:
			raise Exception('UPC fixture already exists.')
	
	data = data.split('\n')
	header = data.pop(0).split(',')
	
	#get column indices
	try:
		index_grp_id = header.index('grp_id')
		index_upc = header.index('upc14')
		index_brand = header.index('brand')
		index_name = header.index('name')
	except:
		raise Exception('Data does not contain all necessary columns.')
	
	with open(output_file_path, 'w') as output_file:
		
		output_file.write('[')
		
		delimiter = ''
		for row in data:
			columns = row.split(',')
			if len(columns) < max(index_grp_id, index_upc, index_brand, index_name):
				continue
			
			grp_id = columns[index_grp_id]
			brand = columns[index_brand][:50]
			name = columns[index_name][:100]
			upc = columns[index_upc]
			
			if '\'' in name or '\"' in name:
				name = name.replace('\'', '').replace('\"', '')
			if '\'' in brand or '\"' in brand:
				brand = brand.replace('\'', '').replace('\"', '')
			
			json_string = delimiter + write_upc_json(grp_id, brand, name, upc)
			output_file.write(json_string)
			delimiter = ','
		
		output_file.write(']')


def write_upc_json(grp_id, brand, name, upc):
	template = """
	{{
		"model": "inventory.opengrocerydatabaseentry",
		"pk": {0},
		"fields": {{
			"grp_id": {0},
			"product_brand": "{1}",
			"product_name": "{2}",
			"product_upc": {3}
		}}
	}}
	"""
	rendered = template.format(grp_id, brand, name, int(upc))
	return rendered


if __name__ == '__main__':
	build_fixtures()

