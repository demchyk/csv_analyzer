import sqlite3
import pandas as pd
import numpy as np
import os
from numba import jit
pd.set_option('use_inf_as_na', True)

class DataBasa:


	def __init__(self,zte_object,table_name,nodes_tigger):
		self.__headers = zte_object.headers
		self.__metrics = zte_object.metrics
		self.__primary_keys = zte_object.primary_keys
		self.__counters = zte_object.counters
		self.__nodes = zte_object.nodes
		self.__nodes_trigger = nodes_tigger
		self.__db_name = 'DB/basa.db'
		self.__table_name = table_name
		self.__connection = sqlite3.connect(self.__db_name, isolation_level=None)
		self.__cursor = self.__connection.cursor()
		self.__files_path = zte_object.files_path
		self.__data_time_field_name = self.__primary_keys[0]
		self.__counters_group_by_frequency = 'D'
		self.__node_group_by_name = zte_object.nodes_key
		self.__class__.__create_initial_table(self.__cursor, self.__table_name, self.__primary_keys, self.__counters,self.__connection)


	@staticmethod
	def __create_initial_table(cur,table_name,primary_keys,counters,conn):
		query = f'''CREATE TABLE IF NOT EXISTS {table_name} (
			{','.join((lambda x: "'"+x+"'")(x) for x in(primary_keys+counters))},
			PRIMARY KEY ({','.join((lambda x: "'"+x+"'")(x) for x in(primary_keys))})
			);'''
		cur.execute(query)


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


	@staticmethod
	def __remover_collecttime_from_primary_keys(primary_keys,data_time_field_name):
		copy_list = primary_keys[:]
		copy_list.remove(data_time_field_name)
		return copy_list

	@jit
	def result_to_sql(self):	
		grouped_counters = self.__data_frame_processing(self.__counters,self.__files_path,self.__primary_keys,self.__data_time_field_name,self.__counters_group_by_frequency,self.__nodes,self.__nodes_trigger,self.__node_group_by_name)
		grouped_counters.to_sql('temp', self.__connection, if_exists = 'replace', index = False)
		self.__cursor.execute(f''' INSERT OR IGNORE INTO {self.__table_name} SELECT * FROM temp''')
		self.__cursor.execute(''' DROP TABLE IF EXISTS temp ''')
		grouped_counters = grouped_counters.groupby(['COLLECTTIME','SITEID'], as_index = False).sum()
		final_table = self.__calculate_final_table_with_metrics(self.__metrics,self.__counters,grouped_counters.copy(),['COLLECTTIME','SITEID'])
		# final_table.to_sql('level-2',self.__connection, if_exists = 'replace', index = False)
		final_table.to_csv('level-2.csv', index = False)
		grouped_counters = grouped_counters.groupby(['COLLECTTIME'], as_index = False).sum()
		final_table = self.__calculate_final_table_with_metrics(self.__metrics,self.__counters,grouped_counters.copy(),['COLLECTTIME','SITEID'])
		# final_table.to_sql('level-3',self.__connection, if_exists = 'replace', index = False)
		final_table.to_csv('level-1.csv', index = False)
		self.__connection.close()

	@classmethod
	def __data_frame_processing(cls,counters,files_path,primary_keys,data_time_field_name,counters_group_by_frequency,nodes,check_for_nodes,node_group_by_name):
		grouped_counters = cls.__generate_concated_temp_data_frame(counters,files_path,primary_keys)
		grouped_counters = cls.__group_data_frame_by_primary_keys(grouped_counters,primary_keys)
		grouped_counters[data_time_field_name] = cls.__set_data_time_format_for_dataframe(data_time_field_name,grouped_counters)
		grouped_counters = cls.__group_counters_by_frequency(primary_keys,grouped_counters,data_time_field_name,counters_group_by_frequency)
		if check_for_nodes:
			grouped_counters = cls.__get_only_special_nodes(grouped_counters,nodes,node_group_by_name)

		return grouped_counters

	@classmethod
	def __generate_concated_temp_data_frame(cls,counters,files_path,primary_keys):
		temp_data_frame_list = cls.__fill_temp_data_frame_list(files_path,primary_keys, counters)
		concated_data_frames = pd.concat(temp_data_frame_list)
		return concated_data_frames

	@staticmethod
	def __group_data_frame_by_primary_keys(concated_data_frames,primary_keys):
		grouped_counters = concated_data_frames.groupby(primary_keys, as_index=False).max()
		return grouped_counters

	@staticmethod
	def __get_only_special_nodes(grouped_counters,nodes,node_group_by_name):
		new_df = grouped_counters[grouped_counters[node_group_by_name].isin(nodes)]
		return new_df
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
			grouped_counters[key] = np.around(eval(value),2)
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


