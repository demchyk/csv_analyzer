from unpacking_folders import *
from metric_counters import *
from databasa import *
import time
start_time = time.time()

path = os.path.abspath(os.curdir)
cur_folder = Folder(path)
file = 'formula.txt'
keys = 'GSM_PKEY.txt'
zek = 'test.csv'
GSM = ZTE_Object(file,keys,cur_folder)
db = DataBasa(GSM,'basa','table')

# @timer
# def starter(files_path):	
# 	for item in os.listdir(files_path):
# 		db.fill_table(files_path+'/'+item)

db.result_to_sql()
print("--- %s seconds ---" % (time.time() - start_time))
# db.fill_table(zek)
# starter(GSM.files_path)
# db.result_to_sql()
# db.gather_values()