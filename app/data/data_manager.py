import pickle
import sys
import os 


def get_file_path(relative_path : str) -> str:
	'''Get absolute path to resource'''
	bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
	if not (getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')): bundle_dir = bundle_dir[:len(bundle_dir) - 4]
	return os.path.join(bundle_dir, relative_path)


def get_data(file_name : str) -> dict:
	return pickle.load(open(get_file_path(file_name), 'rb'))


def write_data(file_name, data) -> None:
	file = open(get_file_path(file_name), 'wb') # wb - w = write b = bytemode
	pickle.dump(data, file) 
	file.close()

def get_wordle_data(file_name: str) -> dict[str,dict[str, list[str]]]:
	'''
	Wordle data dict fortmat
	
	{
		'language' : {
			'used_words' : [],
			'words' : []
		}
	}
	
	'''
	return get_data(file_name)

