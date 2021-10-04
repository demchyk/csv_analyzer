class ZTE_Object:

	
	def __init__(self, folder_object):
		self.__files_path = folder_object.csv_path
		self.__instructions_file = folder_object.formula
		self.__primary_keys_file = folder_object.keys
		self.__nodes_file = folder_object.nodes
		self.__counters = self.__class__.__extract_counters_from_formulas(self.__instructions_file)
		self.__metrics = self.__class__.__extract_metrics_from_file(self.__instructions_file)
		self.__primary_keys = self.__class__.__extract_primary_keys_from_file(self.__primary_keys_file)
		self.__nodes = self.__class__.__extract_nodes_from_file(self.__nodes_file)[1:]
		self.__nodes_key = self.__class__.__extract_nodes_from_file(self.__nodes_file)[0]
		self.__headers = ','.join(self.__primary_keys + self.__counters)


	@staticmethod
	def __extract_formulas_from_file(instructions_file):
		with open(instructions_file,'rt') as f:
			formulas = [formulas_temp.strip() for formulas_temp in f.readlines() if not formulas_temp.isspace()]
		return formulas

	@staticmethod
	def __extract_primary_keys_from_file(primary_keys_file):
		with open(primary_keys_file,'rt') as f:
			primary_keys = [keys_temp.strip() for keys_temp in f.readlines() if not keys_temp.isspace()]
		return primary_keys

	@staticmethod
	def __extract_nodes_from_file(nodes_file):
		with open(nodes_file,'rt') as f:
			nodes = [nodes_temp.strip() for nodes_temp in f.readlines() if not nodes_temp.isspace()]
		return nodes	


	@classmethod
	def __extract_metrics_from_file(cls,instructions_file):
		metrica_dic = {}
		formulas = cls.__extract_formulas_from_file(instructions_file)
		for formula in formulas:
			metrica = formula[:formula.find('=')].strip()
			expression = formula[formula.find('=') + 1:]
			metrica_dic[metrica] = expression.strip()
		return metrica_dic

	@classmethod
	def __extract_counters_from_formulas(cls,instructions_file):
		formulas = cls.__extract_formulas_from_file(instructions_file)
		all_counters = []
		for formula in formulas:
			expression = formula[formula.find('=') + 1:]
			bad_words = '+-/*:.,()!@#$%^&'
			for word in bad_words:
				expression = expression.replace(word,' ')
			text_list = [word.strip() for word in expression.split() if word[0].isalpha() and word[1:].isdigit()]
			all_counters += (text_list)
		return list(set(all_counters))


	@property
	def counters(self):
		return self.__counters
	@property
	def metrics(self):
		return self.__metrics
	@property
	def primary_keys(self):
		return self.__primary_keys
	@property
	def headers(self):
		return self.__headers
	@property
	def files_path(self):
		return self.__files_path
	@property
	def nodes(self):
		return self.__nodes
	@property
	def nodes_key(self):
		return self.__nodes_key
