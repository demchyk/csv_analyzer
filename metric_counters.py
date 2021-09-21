from unpacking_folders import *

class ZTE_Object:

	
	def __init__(self,instructions_file,primary_keys_file, folder_object):
		self.__counters = self.__class__.__extract_counters_from_formulas(instructions_file)
		self.__metrics = self.__class__.__extract_metrics_from_file(instructions_file)
		self.__primary_keys = self.__class__.__extract_primary_keys_from_file(primary_keys_file)
		self.__headers = ','.join(self.__primary_keys + self.__counters)
		self.__files_path = folder_object.result_path

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
			bad_words = '+-/*:.,()'
			for word in bad_words:
				expression = expression.replace(word,' ')
			text_list = [word.strip() for word in expression.split()]
		all_counters.append(text_list[1:])
		return list(set(all_counters[0]))

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

 			
