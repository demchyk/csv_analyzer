import pandas as pd
import numpy as np
from zipfile import ZipFile
from . import multipotok
from functools import partial
pd.set_option('use_inf_as_na', True)

class DataBasa:

	node_cell_dict = {'GSMV3':['SITEID','BTSNAME'],'LTE':['ENODEBID','CELLNAME'],'WCDMA':['NODEBID','CELLNAME']}

	def __init__(self,zte_object,table_name):
		self.__metrics = zte_object.metrics
		self.__metrics_names = zte_object.metrics_names
		self.__primary_keys = zte_object.primary_keys
		self.__counters = zte_object.counters
		self.__ZTE_type = table_name
		self.__table_name = 'DB/' + table_name + '.pkl'
		self.__zipfiles_list_list = zte_object.zipfiles_list
		self.__data_time_field_name = self.__primary_keys[0]
		self.__counters_group_by_frequency = 'H'
		self.__node_name = self.__class__.node_cell_dict[table_name][0]
		self.__cell_name = self.__class__.node_cell_dict[table_name][1]

	def result_to_pickle(self):
		grouped_counters_list = []
		for zip_file_list in self.__zipfiles_list_list:
			grouped_counters = self.__data_frame_processing(self.__counters,self.__primary_keys,self.__data_time_field_name,self.__counters_group_by_frequency,zip_file_list,self.__ZTE_type)
			grouped_counters_list.append(grouped_counters)
		new_pickle = pd.concat(grouped_counters_list)
		new_pickle = self.__append_cellname_to_wcdma(self.__ZTE_type,new_pickle,self.__primary_keys)		
		try:
			new_pickle = pd.concat([new_pickle,pd.read_pickle(self.__table_name,compression = 'zip')]).drop_duplicates().reset_index()
		except:
			pass
		finally:
			if not new_pickle.attrs:
				new_pickle.attrs = self.__get_attr_for_dataframe(self.__ZTE_type,self.__node_name,self.__cell_name,self.__data_time_field_name,self.__metrics_names,self.__metrics,self.__primary_keys,self.__counters)
			new_pickle.to_pickle(self.__table_name,compression = 'zip')

	@staticmethod
	def __get_attr_for_dataframe(zte_type,node_name,cell_name,data_time_field_name,metrics_names,metrics,primary_keys,counters):
		attr_dict = {}
		attr_dict['zte_type'] = zte_type
		attr_dict['node_name'] = node_name
		attr_dict['cell_name'] = cell_name
		attr_dict['data_time_field_name'] = data_time_field_name
		attr_dict['metrics'] = metrics
		attr_dict['metrics_names'] = metrics_names
		attr_dict['primary_keys'] = primary_keys
		attr_dict['counters'] = counters
		return attr_dict		

	@classmethod
	def _fill_temp_data_frame_list(cls,counters,zip_list,primary_keys,table_name):
		df_list = []
		read_zip_partial = partial(cls._read_zip,primary_keys,counters,table_name)
		df_list_of_list = multipotok.parmap(read_zip_partial,zip_list)
		for df_list_elem in df_list_of_list:
			if df_list_elem:
				df_list += df_list_elem
		return df_list

	@staticmethod
	def _read_csv(file,primary_keys,counters,table_name):
		data_frame_from_csv = pd.read_csv(file)
		if not data_frame_from_csv.empty:
			df_columns = data_frame_from_csv.columns.tolist()
			final_list = list(set(counters) & set(data_frame_from_csv.columns.tolist()))
			if final_list:			
				if table_name == 'WCDMA':
					if 'CELLNAME' in df_columns:
						data_frame_from_csv = data_frame_from_csv[primary_keys + final_list]
					else:
						cutted_primary_keys = primary_keys.copy()
						cutted_primary_keys.remove('CELLNAME')
						data_frame_from_csv = data_frame_from_csv[cutted_primary_keys + final_list]
					return data_frame_from_csv

				data_frame_from_csv = data_frame_from_csv[primary_keys + final_list]
				return data_frame_from_csv
			pass
		pass

	@classmethod
	def _read_zip(cls,primary_keys,counters,table_name,file):
		try:
			return [cls._read_csv(ZipFile(file).open(i),primary_keys,counters,table_name) for i in ZipFile(file).filelist if i.file_size > 2500]
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

	@classmethod
	def __data_frame_processing(cls,counters,primary_keys,data_time_field_name,counters_group_by_frequency,zip_list,table_name):
		grouped_counters = cls.__generate_concated_temp_data_frame(counters,zip_list,primary_keys,table_name)
		grouped_counters = cls.__group_data_frame_by_primary_keys(grouped_counters,primary_keys)
		grouped_counters[data_time_field_name] = cls.__set_data_time_format_for_dataframe(data_time_field_name,grouped_counters)
		grouped_counters = cls.__group_counters_by_frequency(primary_keys,grouped_counters,data_time_field_name,counters_group_by_frequency)
		return grouped_counters

	@classmethod
	def __generate_concated_temp_data_frame(cls,counters,zip_list,primary_keys,table_name):
		temp_data_frame_list = cls._fill_temp_data_frame_list(counters,zip_list,primary_keys,table_name)
		concated_data_frames = pd.concat(temp_data_frame_list)
		return concated_data_frames

	@staticmethod
	def __group_data_frame_by_primary_keys(concated_data_frames,primary_keys):
		grouped_counters = concated_data_frames.groupby(primary_keys, as_index=False,dropna = False).max()
		return grouped_counters

	@staticmethod
	def __set_data_time_format_for_dataframe(data_time_field_name,grouped_counters):
		return pd.to_datetime(grouped_counters[data_time_field_name], format = '%Y%m%d%H%M')

	@classmethod
	def __group_counters_by_frequency(cls,primary_keys,grouped_counters,data_time_field_name,frequency):
		cutted_primary_keys = cls.__remover_collecttime_from_primary_keys(primary_keys,data_time_field_name)
		grouped_counters = grouped_counters.groupby([pd.Grouper(key = data_time_field_name, freq = frequency)] + cutted_primary_keys,dropna = False).sum()
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
	def __append_cellname_to_wcdma(table_name,df,primary_keys):
		if not table_name == 'WCDMA':
			return df
		temp_df_cellname = df[['CELLID','CELLNAME']].dropna().drop_duplicates()
		df.drop(['CELLNAME'],axis = 1,inplace = True)
		cutted_primary_keys = primary_keys.copy()
		cutted_primary_keys.remove('CELLNAME')
		df = df.groupby(cutted_primary_keys,as_index = False).sum()
		return df.merge(temp_df_cellname,how = 'left')


