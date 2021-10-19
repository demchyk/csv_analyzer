import pandas as pd
import numpy as np
import time
class Aggregation:


	def __init__(self,date_range,claster_check,aggregation_time_type=None,aggregation_type=None):
		self.__df = self.__class__.__create_df_from_temp_pickle()
		self.__metrics = self.__df.attrs['metrics']
		self.__metrics_names = self.__df.attrs['metrics_names']
		self.__primary_keys = self.__df.attrs['primary_keys']
		self.__counters = self.__df.attrs['counters']
		self.__ZTE_type = self.__df.attrs['zte_type']
		self.__data_time_field_name = self.__df.attrs['data_time_field_name']	
		self.__node_name = self.__df.attrs['node_name']
		self.__cell_name = self.__df.attrs['cell_name']
		self.__report_file_name = 'ZTE/' + self.__ZTE_type + '/reports/' + self.__ZTE_type
		self.__table_name = 'DB/' + self.__ZTE_type + '.pkl'
		self.__claster_check = claster_check
		self.__date_range = date_range
		self.__aggregation_time_type = aggregation_time_type
		self.__aggregation_type = aggregation_type

	@staticmethod
	def __create_df_from_temp_pickle():
		return pd.read_pickle('DB/export_to_csv.temp',compression = 'zip')

	@classmethod
	def __agg_by_time(cls,df,primary_keys,data_time_field_name,frequency,metrics):
		if not frequency == 'H':
			cutted_primary_keys = cls.__remover_collecttime_from_primary_keys(primary_keys,data_time_field_name)
			df = df.groupby([pd.Grouper(key = data_time_field_name, freq = frequency)] + cutted_primary_keys).sum()
			df.reset_index(inplace = True)
			return df
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
	def __swap_counters_for_metrics(cls,df,metrics,counters):
		renamed_metrics = cls.__rename_metrics_for_usage(metrics,counters)
		df_columns = df.columns.tolist()
		primary_keys = [key for key in df_columns if key not in counters]
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

	@staticmethod
	def __agg_by_type(df,aggregation_type,node_name,data_time_field_name,counters):
		if aggregation_type == 'CELL':
			return df
		if aggregation_type == 'NODE':
			df_fields = [data_time_field_name,node_name] + counters
			return df.groupby([data_time_field_name,node_name],as_index = False).sum()[df_fields]
		if aggregation_type == 'CLUSTER':
			df_fields = [data_time_field_name,'CLUSTER'] + counters 
			df = df[df[claster_name].astype(str).isin(claster_values)].groupby(data_time_field_name,as_index = False).sum()
			df['CLUSTER'] = 'CLUSTER'
			return df[df_fields]
			# new_df['CLUSTER'] = 'CLUSTER'
			# return new_df

	@staticmethod
	def __get_claster_info(df):
		cluster_file = f'ZTE/{df.attrs["zte_type"]}/requirements/cluster.txt'
		with open(cluster_file,'rt') as f:
			nodes = [nodes_temp.strip() for nodes_temp in f.readlines() if not nodes_temp.isspace()]
		return nodes[0],nodes[1:]	

	@classmethod
	def __apply_claster(cls,df,claster_check):
		if claster_check == 'cluster':
			claster_name,claster_values = cls.__get_claster_info(df)
			return df[df[claster_name].astype(str).isin(claster_values)]
		return df


	def aggregate_to_csv(self):
		time1 = time.time()
		dframe = self.__agg_by_date_interval(self.__df,self.__date_range,self.__data_time_field_name)
		print(time.time() - time1)
		dframe = self.__agg_by_time(dframe,self.__primary_keys,self.__data_time_field_name,self.__aggregation_time_type,self.__metrics)
		print(time.time() - time1)
		dframe = self.__apply_claster(dframe,self.__claster_check)
		print(time.time() - time1)
		dframe = self.__agg_by_type(dframe,self.__aggregation_type,self.__node_name,self.__data_time_field_name,self.__counters)
		print(time.time() - time1)
		dframe = self.__swap_counters_for_metrics(dframe,self.__metrics,self.__counters)
		print(time.time() - time1)
		dframe.to_csv((f'{self.__report_file_name}-{self.__date_range}-{self.__aggregation_type}-{self.__aggregation_time_type}.csv').replace(' ',''))		

	def aggregate_to_dataframe(self):
		dframe = self.__agg_by_date_interval(self.__df.copy(),self.__date_range,self.__data_time_field_name)
		dframe = self.__apply_claster(dframe,self.__claster_check,self.__claster_name,self.__claster_values)
		dframe = self.__swap_counters_for_metrics(dframe,self.__metrics,self.__counters)
		dframe.to_pickle('DB/dashboard.temp',compression = 'zip')
