import sqlite3
import pandas as pd
from metric_counters import *


class DataBasa:


	def __init__(self,zte_object,db_name,table_name):
		self.__headers = zte_object.headers
		self.__metrics = zte_object.metrics
		self.__primary_keys = zte_object.primary_keys
		self.__counters = zte_object.counters
		self.__db_name = str(db_name)+'.db'
		self.__table_name = table_name
		self.__connection, self.__cursor = self.__class__.__init_db_connection(self.__db_name)
		self.__files_path = zte_object.files_path


	@staticmethod
	def __init_db_connection(db_name):
		return sqlite3.connect(db_name),sqlite3.connect(db_name).cursor()

	@classmethod
	def __fill_temp_data_frame_list(cls,path,primary_keys,counters):
		temp_data_frame_list = []
		for file_from_path in os.listdir(path):
			file = path + '/' + file_from_path
			useful_values_from_csv = cls.__get_useful_values_from_csv(file,primary_keys,counters)
			if not useful_values_from_csv:
				pass
			else:
				data_frame_from_csv = pd.read_csv(file, usecols = useful_values_from_csv + primary_keys)
				temp_data_frame_list.append(data_frame_from_csv)
		return temp_data_frame_list

	@staticmethod
	def __rename_metrics_for_usage(metrics,counters):
		new_dict = {}
		for key,value in metrics.items():
			new_value = value
			for counter in counters:
				new_value = new_value.replace(counter,'grouped_counters["' + counter + '"]')
			new_dict[key] = new_value
		return new_dict


	def result_to_sql(self):
		metrics = self.__rename_metrics_for_usage(self.__metrics,self.__counters)
		temp_data_frame_list = self.__fill_temp_data_frame_list(self.__files_path, self.__primary_keys, self.__counters)
		concated_data_frames = pd.concat(temp_data_frame_list)
		grouped_counters = concated_data_frames.groupby(self.__primary_keys).max()
		for key,value in metrics.items():
			grouped_counters[key] = eval(value)
		grouped_counters.reset_index(inplace = True)
		final_table = grouped_counters[self.__primary_keys + list(self.__metrics.keys())]
		final_table.to_sql('semi_temp',self.__connection, if_exists = 'append', index = False)

	@staticmethod
	def __get_useful_values_from_csv(file,primary_keys,counters):	
		file_header_values = pd.read_csv(file, nrows = 0).columns.tolist()
		if not all(key in file_header_values for key in primary_keys):
			return False
		else:
			useful_values = []
			for value in file_header_values:
				if value in counters:
					useful_values.append(value)
			return useful_values

	def close_connection(self):
		self.__connection.close()

