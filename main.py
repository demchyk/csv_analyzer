from unpacking_folders import *
from metric_counters import *
from databasa import *


path = os.path.abspath(os.curdir)
cur_folder = Folder(path)
file = 'formula.txt'
keys = 'GSM_PKEY.txt'
zek = 'test.csv'
GSM = ZTE_Object(file,keys,cur_folder)
db = DataBasa(GSM,'basa','table')

for item in os.listdir(GSM.files_path):
	db.fill_table(GSM.files_path+'/'+item)
db.close_connection()

