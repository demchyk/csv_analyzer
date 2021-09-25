import sqlite3
import pandas as pd
from metric_counters import *
import time

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

	def gather_values(self):
		query = f''' SELECT {','.join(self.__primary_keys)},{','.join(['MAX(' + elem.strip() + ')' + 'AS ' + elem for elem in self.__counters])} FROM {self.__table_name + '_temp'} GROUP BY {','.join(self.__primary_keys)}'''
		self.__cursor.execute(f''' CREATE TABLE IF NOT EXISTS {self.__table_name + '_notemo'} AS {query}''')


	def fill_table(self,file):
		useful_values_from_csv = self.__get_useful_values_from_csv(file,self.__primary_keys,self.__counters)
		if not useful_values_from_csv:
			# print('Sorry')
			pass
		else:
			try:
				self.__cursor.execute(f''' CREATE TABLE IF NOT EXISTS {self.__table_name + '_temp'} ({self.__headers}) ''')
				data_frame_from_csv = pd.read_csv(file, usecols = useful_values_from_csv + self.__primary_keys)
				data_frame_from_csv = data_frame_from_csv.fillna(0)
				data_frame_from_csv.to_sql(self.__table_name + '_temp', self.__connection, if_exists = 'append',index = False)
				self.__connection.commit()
			except sqlite3.IntegrityError:
				print('Повторяемся') #need to skip

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

