import sqlite3
import pandas as pd
import numpy as np
import math
conn = sqlite3.connect('basa.db')
cur = conn.cursor()


# a = ['MAX(' + elem.strip() + ')' + 'AS ' + elem for elem in a.split(',')]

# q = f''' SELECT COLLECTTIME,BTSNAME,SITEID, {",".join(a)} FROM table_temp GROUP BY COLLECTTIME,BTSNAME,SITEID  '''

# df = pd.read_sql_query(q,conn)
# df.fillna(0,inplace=True)

pd.set_option('use_inf_as_na', True)
df = pd.read_sql_query('SELECT * from semi_temp', conn)
df = df.groupby([pd.Grouper(key = 'COLLECTTIME', freq = 'd')] + ['BTSNAME']).sum()
df.to_sql('chekout',conn,if_exists = 'replace', index = False)


a = '202109140000'

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

