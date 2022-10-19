import pickle
import sys
import os 


'''
Wordle data dict fortmat

{
	'language' : {
		'used_words' : [],
		'words' : []
	}
}

'''
def get_file_path(relative_path):
	'''Get absolute path to resource'''
	bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
	return os.path.join(bundle_dir, relative_path)


def get_data(file_name):
	return pickle.load(open(get_file_path(file_name), 'rb'))


def write_data(file_name, data):
	file = open(get_file_path(file_name), 'wb') # wb - w = write b = bytemode
	pickle.dump(data, file) 
	file.close()


