from unpacking_folders import *
from metric_counters import *
from databasa import *
import time

def timer(func):
    def wrapper(*args):
        start = time.time()
        func(*args)
        end = time.time()
        print('[*] Время выполнения: {} секунд.'.format(end-start))
    return wrapper


path = os.path.abspath(os.curdir)
cur_folder = Folder(path)
file = 'formula.txt'
keys = 'GSM_PKEY.txt'
zek = 'test.csv'
GSM = ZTE_Object(file,keys,cur_folder)
print(GSM.counters)
db = DataBasa(GSM,'basa','table')

@timer
def starter(files_path):	
	for item in os.listdir(files_path):
		db.fill_table(files_path+'/'+item)

# db.fill_table(zek)
starter(GSM.files_path)
db.gather_values()