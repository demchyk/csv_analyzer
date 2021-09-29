import sqlite3
import pandas as pd
import numpy as np
from metric_counters import *
pd.set_option('use_inf_as_na', True)

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
		self.__data_time_field_name = 'COLLECTTIME'


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
				data_frame_from_csv = pd.read_csv(file, usecols = useful_values_from_csv + primary_keys, )
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


	@staticmethod
	def __remover_collecttime_from_primary_keys(primary_keys,data_time_field_name):
		copy_list = primary_keys[:]
		copy_list.remove(data_time_field_name)
		return copy_list

	def result_to_sql(self):
		concated_data_frames = self.__generate_concated_temp_data_frame(self.__counters,self.__files_path,self.__primary_keys)
		grouped_counters = self.__group_data_frame_by_primary_keys(concated_data_frames,self.__primary_keys)
		grouped_counters[self.__data_time_field_name] = self.__set_data_time_format_for_dataframe(self.__data_time_field_name,grouped_counters)
		grouped_counters = self.__group_counters_by_frequency(self.__primary_keys,grouped_counters,self.__data_time_field_name,'D')
		final_table = self.__calculate_final_table_with_metrics(self.__metrics,self.__counters,grouped_counters,self.__primary_keys)	
		final_table.to_sql('semi_temp',self.__connection, if_exists = 'append', index = False)
		self.__connection.close()

	@classmethod
	def __generate_concated_temp_data_frame(cls,counters,files_path,primary_keys):
		temp_data_frame_list = cls.__fill_temp_data_frame_list(files_path,primary_keys, counters)
		concated_data_frames = pd.concat(temp_data_frame_list)
		return concated_data_frames

	@staticmethod
	def __group_data_frame_by_primary_keys(concated_data_frames,primary_keys):
		grouped_counters = concated_data_frames.groupby(primary_keys).max()
		grouped_counters.reset_index(inplace = True)
		return grouped_counters

	@staticmethod
	def __set_data_time_format_for_dataframe(data_time_field_name,grouped_counters):
		return pd.to_datetime(grouped_counters[data_time_field_name], format = '%Y%m%d%H%M')

	@classmethod
	def __group_counters_by_frequency(cls,primary_keys,grouped_counters,data_time_field_name,frequency):
		cutted_primary_keys = cls.__remover_collecttime_from_primary_keys(primary_keys,data_time_field_name)
		grouped_counters = grouped_counters.groupby([pd.Grouper(key = data_time_field_name, freq = frequency)] + cutted_primary_keys).sum()
		grouped_counters.reset_index(inplace = True)
		return grouped_counters

	@classmethod
	def __calculate_final_table_with_metrics(cls,metrics,counters,grouped_counters,primary_keys):
		renamed_metrics = cls.__rename_metrics_for_usage(metrics,counters)
		for key,value in renamed_metrics.items():
			grouped_counters[key] = np.ceil(eval(value))
		final_table = grouped_counters[primary_keys + list(metrics.keys())]
		return final_table

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


