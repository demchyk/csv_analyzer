import pandas as pd
import numpy as np
from zipfile import ZipFile
import multipotok
from functools import partial
import shutil
import os
pd.set_option('use_inf_as_na', True)

class DataBasa:
	def __init__(self,zte_object,table_name):
		self.__headers = zte_object.headers
		self.__metrics = zte_object.metrics
		self.__primary_keys = zte_object.primary_keys
		self.__counters = zte_object.counters
		self.__table_name = 'DB/' + table_name + '.pkl'
		self.__table_temp_name = 'DB/' + table_name + '_reserved.pkl'
		self.__zipfiles_list_list = zte_object.zipfiles_list
		self.__data_time_field_name = self.__primary_keys[0]
		self.__counters_group_by_frequency = 'H'


	@classmethod
	def __fill_temp_data_frame_list(cls,counters,zip_list,primary_keys):
		df_list = []
		read_zip_partial = partial(cls.__read_zip,primary_keys,counters)
		df_list_of_list = multipotok.parmap(read_zip_partial,zip_list)
		for df_list_elem in df_list_of_list:
			df_list += df_list_elem
		return df_list

	@staticmethod
	def __read_csv(file,primary_keys,counters):
		data_frame_from_csv = pd.read_csv(file)
		df_columns = data_frame_from_csv.columns.tolist()
		if not all(key in df_columns for key in primary_keys):
			pass
		else:
			final_list = list(set(counters) & set(data_frame_from_csv.columns.tolist()))
			if final_list:
				data_frame_from_csv = data_frame_from_csv[primary_keys + final_list]
				return data_frame_from_csv
			pass

	@classmethod
	def __read_zip(cls,primary_keys,counters,file):
		try:
			return [cls.__read_csv(ZipFile(file).open(i),primary_keys,counters) for i in ZipFile(file).namelist()]
		except:
			pass

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

	def result_to_pickle(self):

		for zip_file_list in self.__zipfiles_list_list:
			grouped_counters = self.__data_frame_processing(self.__counters,self.__primary_keys,self.__data_time_field_name,self.__counters_group_by_frequency,zip_file_list)
			try:
				pd.read_pickle(self.__table_name,compression = 'zip')
			except:
				pass
			else:
				grouped_counters = pd.concat([grouped_counters,pd.read_pickle(self.__table_name,compression = 'zip')]).drop_duplicates().reset_index(drop=True)
			finally:
				grouped_counters.to_pickle(self.__table_name,compression = 'zip')


	@classmethod
	def __data_frame_processing(cls,counters,primary_keys,data_time_field_name,counters_group_by_frequency,zip_list):
		grouped_counters = cls.__generate_concated_temp_data_frame(counters,zip_list,primary_keys)
		grouped_counters = cls.__group_data_frame_by_primary_keys(grouped_counters,primary_keys)
		grouped_counters[data_time_field_name] = cls.__set_data_time_format_for_dataframe(data_time_field_name,grouped_counters)
		grouped_counters = cls.__group_counters_by_frequency(primary_keys,grouped_counters,data_time_field_name,counters_group_by_frequency)
		return grouped_counters

	@classmethod
	def __generate_concated_temp_data_frame(cls,counters,zip_list,primary_keys):
		temp_data_frame_list = cls.__fill_temp_data_frame_list(counters,zip_list,primary_keys)
		concated_data_frames = pd.concat(temp_data_frame_list)
		return concated_data_frames

	@staticmethod
	def __group_data_frame_by_primary_keys(concated_data_frames,primary_keys):
		grouped_counters = concated_data_frames.groupby(primary_keys, as_index=False).max()
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


