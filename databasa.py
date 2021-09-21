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


	@staticmethod
	def __init_db_connection(db_name):
		return sqlite3.connect(db_name),sqlite3.connect(db_name).cursor()



	def fill_table(self,file):
		if not self.__check_csv(file,self.__primary_keys,self.__counters):
			print('Sorry')
		else:
			try:
				self.__cursor.execute(f''' CREATE TABLE IF NOT EXISTS {self.__table_name + '_temp'} ({self.__headers},primary key ({",".join(self.__primary_keys)})) ''')
				useful_values_from_csv = self.__get_useful_values_from_csv(file,self.__counters) + self.__primary_keys
				data_frame_from_csv = pd.read_csv(file, usecols = useful_values_from_csv)
				data_frame_from_csv.to_sql(self.__table_name + '_temp', self.__connection, if_exists = 'append',index = False)
				self.__connection.commit()
			except sqlite3.IntegrityError:
				print('Повторяемся') #need to skip


	@staticmethod
	def __check_csv(file,primary_keys,counters):
		file_header_values = pd.read_csv(file, nrows = 0).columns.tolist()
		if not all(key in file_header_values for key in primary_keys):
			return False #Не все ключи присутствуют, скипаем
		else:
			for value in file_header_values:
				if value in counters:
					return True
			return False

	@staticmethod
	def __get_useful_values_from_csv(file,counters):
		useful_values = []
		file_header_values = pd.read_csv(file, nrows = 0).columns.tolist()
		for value in file_header_values:
			if value in counters:
				useful_values.append(value)
		return useful_values

	def close_connection(self):
		self.__connection.close()
