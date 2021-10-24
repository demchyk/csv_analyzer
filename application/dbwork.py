import pandas as pd
import dask
import dask.dataframe as dd
import time


# a = ['MAX(' + elem.strip() + ')' + 'AS ' + elem for elem in a.split(',')]

# q = f''' SELECT COLLECTTIME,BTSNAME,SITEID, {",".join(a)} FROM table_temp GROUP BY COLLECTTIME,BTSNAME,SITEID  '''

# df = pd.read_sql_query(q,conn)
# df.fillna(0,inplace=True)
# engine = db.create_engine('sqlite:///DB/basa.sqlite')
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





# q = (f''' SELECT COLLECTTIME,BTSNAME,SITEID, {Call_Completion} AS CALL, {DL_Qual} AS BALL, {DL_TBF_SR} AS RALL  FROM table_notemo ''')
# df = pd.read_sql_query(q,conn)
# df.to_sql('metrics',conn, if_exists = 'replace')
# conn.close()
# dic = {'Call_Completion':'100 * (df["C901260063"] + df["C901260088"] + df["C901270063"])'}
# print(list(dic.keys()))
# init_df.to_sql('check',conn)

# FGUCL340_G08A


# def __extract_counters_from_formulas():
# 	with open('formula.txt','rt') as f:
# 		formulas = [formulas_temp.strip() for formulas_temp in f.readlines() if not formulas_temp.isspace()]
# 	all_counters = []
# 	for formula in formulas:
# 		expression = formula[formula.find('=') + 1:]
# 		bad_words = '+-/*:.,()!@#$%^&'
# 		for word in bad_words:
# 			expression = expression.replace(word,' ')
# 		text_list = [word.strip() for word in expression.split() if word[0].isalpha() and word[1:].isdigit()]
# 		all_counters += (text_list)
# 	return list(set(all_counters))


# primary_keys = ['COLLECTTIME','SITEID','BTSNAME']
# with open('nodes.txt') as f:
# 	claster_list = [claster.strip() for claster in f.readlines()]
# claster_name = claster_list[0]
# claster = claster_list[1:]
# time1 = time.time()
# # df = pd.read_sql('tbchk','sqlite:///DB/basa.sqlite',chunksize = 200000)
# # new_df = pd.concat(df)
# # new_df.to_pickle('dframe.pkl')
# df = pd.read_pickle('DB/test.pkl',compression = 'zip')
# print(time.time() - time1)
# # df = pd.concat([df]*2)
# # print(time.time() - time1)
# # joblib.dump(df,'DB/test.pkl')
# df.to_sql('basa2',connection,if_exists = 'replace')
# # df.to_pickle('DB/test.pkl',compression = 'zip')
# print(time.time() - time1)
# # df.to_sql('tbchk',conn,if_exists = 'append', index = False)

# df = pd.read_pickle('/Users/denis/Programming/csv_analyzer/DB/WCDMA.pkl', compression = 'zip')
# df = df.groupby([pd.Grouper(key = 'COLLECTTIME', freq = 'D')] + ['NODEBID','CELLID','CELLNAME'],dropna = False).sum()
# df.reset_index(inplace = True)
# # df  = df.groupby(['COLLECTTIME','NODEBID','CELLID'],as_index = False).sum()
# df.to_csv('check.csv')
# print(df.attrs)
time1 = time.time()
dframe = pd.read_pickle('/Users/denis/Programming/csv_analyzer/DB/GSMV3.pkl', compression = 'zip')

# def agg_by_time(df,primary_keys,data_time_field_name,frequency,metrics):
# 	if not frequency == 'H': # to save time
# 		cutted_primary_keys = remover_collecttime_from_primary_keys(primary_keys,data_time_field_name)
# 		df = df.groupby(pd.TimeGrouper(key='dates', freq='D'),cutted_primary_keys).sum()
# 		return df
# 	return df

# def remover_collecttime_from_primary_keys(primary_keys,data_time_field_name):
# 	copy_list = primary_keys[:]
# 	copy_list.remove(data_time_field_name)
# 	return copy_list

# agg_by_time(dframe,dframe.attrs['primary_keys'],dframe.attrs['data_time_field_name'],'D',dframe.attrs['metrics']).to_csv('export-*.csv')

# # ddf.to_csv('export-*.csv')
# print(time.time() - time1)
# print(df.max().to_string())
# df2 = df[['CELLID','CELLNAME']].dropna().drop_duplicates()
# # df.drop(['CELLNAME'],axis = 1,inplace = True)
# # df = df.merge(df2,how = 'left')
# df = df.groupby([pd.Grouper(key = 'COLLECTTIME', freq = 'D')] + ['NODEBID','CELLID','CELLNAME']).sum()
# df.to_csv('check2.csv')
# df = pd.read_csv('some.csv')



# df = df[df[claster_name].isin(claster)].groupby(claster_name, as_index = False).sum()

# df.to_sql('tbchk',conn,if_exists = 'replace', index = False)
# connection.close()



# counters = __extract_counters_from_formulas()








