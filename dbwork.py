import sqlite3
import pandas as pd
import numpy as np
import math
import sqlalchemy as db
import os
import time
from zipfile import ZipFile

# a = ['MAX(' + elem.strip() + ')' + 'AS ' + elem for elem in a.split(',')]

# q = f''' SELECT COLLECTTIME,BTSNAME,SITEID, {",".join(a)} FROM table_temp GROUP BY COLLECTTIME,BTSNAME,SITEID  '''

# df = pd.read_sql_query(q,conn)
# df.fillna(0,inplace=True)
# engine = db.create_engine('sqlite:///DB/basa.db')
# connection = engine.connect()
# df = pd.read_sql_table('GSM',connection)
# df = df[(df['COLLECTTIME'] >= '2021-09-15') & (df['COLLECTTIME'] <= '2021-09-19')]
# df.to_sql('Timecheck', connection, if_exists = 'replace')


# def read_csv(filename):
#     'converts a filename to a pandas dataframe'
#     return pd.read_csv(filename)
# time1 = time.time()
# files = os.listdir('processed_files')
# os.chdir('processed_files')
# with Pool() as pool:
# 	df = pool.map(read_csv, files)
# print(time.time() - time1)


conn = sqlite3.connect('DB/basa.db')
cur = conn.cursor()



# df = df.fillna(0)

# Call_Completion = '100 * (C901260063 + C901260088 + C901270063 + C901270088 + C901050061)/(C901260020 + C901260069 + C901270020 + C901270069 + C901050060)'
# DL_Qual = '100*(C901120125 + C901120126 + C901120127 + C901120128 + C901120129 + C901120130)/(C901120125 + C901120126 + C901120127 + C901120128 + C901120129 + C901120130 + C901120131 + C901120132)'
# DL_TBF_SR = '100 * ((C901000002 + C901000003 + C901000004 + C901000008 + C901000024 + C901000025 + C901000026 + C901000030 + C901170021 + C901180021 + C901170034 + C901180034 + C901000001 + C901000023) - (C901170008 + C901170037 + C901180008 + C901180037))/(C901000002 + C901000003 + C901000004 + C901000008 + C901000024 + C901000025 + C901000026 + C901000030 + C901170021 + C901180021 + C901170034 + C901180034 + C901000001 + C901000023)'

# q = (f''' SELECT COLLECTTIME,BTSNAME,SITEID, {Call_Completion} AS CALL, {DL_Qual} AS BALL, {DL_TBF_SR} AS RALL  FROM table_notemo ''')
# df = pd.read_sql_query(q,conn)
# df.to_sql('metrics',conn, if_exists = 'replace')
# conn.close()
# dic = {'Call_Completion':'100 * (df["C901260063"] + df["C901260088"] + df["C901270063"])'}
# print(list(dic.keys()))
# init_df.to_sql('check',conn)

# FGUCL340_G08A

time1 = time.time()
def __extract_counters_from_formulas():
	with open('formula.txt','rt') as f:
		formulas = [formulas_temp.strip() for formulas_temp in f.readlines() if not formulas_temp.isspace()]
	all_counters = []
	for formula in formulas:
		expression = formula[formula.find('=') + 1:]
		bad_words = '+-/*:.,()!@#$%^&'
		for word in bad_words:
			expression = expression.replace(word,' ')
		text_list = [word.strip() for word in expression.split() if word[0].isalpha() and word[1:].isdigit()]
		all_counters += (text_list)
	return list(set(all_counters))

def __get_useful_values_from_csv(counters,file):	
	file_header_values = pd.read_csv(file, nrows = 0).columns.tolist()
	useful_values = []
	for value in file_header_values:
		if value in counters:
			useful_values.append(value)
	return useful_values


def __fill_temp_data_frame_list_new(counters,zip_list):
	files_list = os.listdir('processed_files')
	os.chdir('processed_files')
	df_list = []
	# df_list = [read_csv(file) for file in files_list]
	with Pool() as pool:
		df_list_of_list = pool.map(read_zip,zip_list)
	for df_list_elem in df_list_of_list:
		df_list += df_list_elem
	print(time.time() - time1)
	combined_df = pd.concat(df_list,ignore_index=True)
	print(time.time() - time1)
	combined_df = combined_df.groupby(['COLLECTTIME','SITEID','BTSNAME'], as_index = False).max()
	print(time.time() - time1)
	combined_df.to_sql('chcker2',conn, if_exists = 'replace', index = False)
	conn.close()
	print(time.time() - time1)


def read_csv(file):
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

def read_zip(file):
	try:
		return [read_csv(ZipFile(file).open(i)) for i in ZipFile(file).namelist()]
	except:
		pass

def __get_zipfile_list():
    rez = []
    path1 = os.path.dirname(os.path.realpath('__file__'))
    cur_path = path1 + "/processed_files"
    for address, dirs, files in os.walk(cur_path):
        for file in files:
            if file.endswith(".zip"):
                rez.append(os.path.join(address, file))
    return rez


zip_list = __get_zipfile_list()

primary_keys = ['COLLECTTIME','SITEID','BTSNAME']
counters = __extract_counters_from_formulas()
__fill_temp_data_frame_list_new(counters,zip_list)







