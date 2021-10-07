import pandas as pd
import numpy as np

class Aggregation:

	def __init__(self,zte_object,table_name,date_range,aggregation_time_type):
		self.__metrics = zte_object.metrics
		self.__primary_keys = zte_object.primary_keys
		self.__counters = zte_object.counters
		self.__table_name = 'DB/' + table_name + '.pkl'
		self.__data_time_field_name = self.__primary_keys[0]
		self.__df = self.__class__.__create_df_from_pickle(self.__table_name)
		self.__date_range = date_range
		self.__aggregation_time_type = aggregation_time_type


	@staticmethod
	def __create_df_from_pickle(table_name):
		return pd.read_pickle(table_name,compression = 'zip')

	@classmethod
	def __agg_by_time(cls,df,primary_keys,data_time_field_name,frequency,metrics,counters):
		cutted_primary_keys = cls.__remover_collecttime_from_primary_keys(primary_keys,data_time_field_name)
		df = df.groupby([pd.Grouper(key = data_time_field_name, freq = frequency)] + cutted_primary_keys).sum()
		df.reset_index(inplace = True)
		return df

	@staticmethod
	def __remover_collecttime_from_primary_keys(primary_keys,data_time_field_name):
		copy_list = primary_keys[:]
		copy_list.remove(data_time_field_name)
		return copy_list

	@staticmethod
	def __rename_metrics_for_usage(metrics,counters):
		new_dict = {}
		for key,value in metrics.items():
			new_value = value
			for counter in counters:
				new_value = new_value.replace(counter,'df["' + counter + '"].values')
			new_dict[key] = new_value
		return new_dict

	@classmethod
	def __swap_counters_for_metrics(cls,df,metrics,counters,primary_keys):
		renamed_metrics = cls.__rename_metrics_for_usage(metrics,counters)
		for key,value in renamed_metrics.items():
			df[key] = np.around(eval(value),2)
		final_table = df[primary_keys + list(metrics.keys())]
		return final_table

	@staticmethod
	def __agg_by_date_interval(df,date_range,data_time_field_name):
		date_start = date_range.split(' - ')[0]
		date_end = date_range.split(' - ')[1]
		df = df[(df[data_time_field_name] >= date_start) & (df[data_time_field_name] <= date_end)]
		return df



	def start_agg(self):
		dframe = self.__agg_by_date_interval(self.__df.copy(),self.__date_range,self.__data_time_field_name)
		dframe = self.__agg_by_time(dframe,self.__primary_keys,self.__data_time_field_name,self.__aggregation_time_type,self.__metrics,self.__counters)
		dframe = self.__swap_counters_for_metrics(dframe,self.__metrics,self.__counters,self.__primary_keys)
		dframe.to_csv('check.csv')

