import pickle
'''
Wordle data dict fortmat

{
	'language' : {
		'used_words' : [],
		'words' : []
	}
}

'''


def get_data(file_name):
	return pickle.load(open(file_name, 'rb'))


def write_data(file_name, data):
	file = open(file_name, 'wb') # wb - w = write b = bytemode
	pickle.dump(data, file) 
	file.close()