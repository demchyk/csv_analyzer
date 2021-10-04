from unpacking_folders import *
from metric_counters import *
from databasa import *


# cur_folder = Net_Folder(os.path.dirname(os.path.realpath('__file__')) + "/ZTE/LTE")
# GSM = ZTE_Object(cur_folder)
# db = DataBasa(GSM,'basa','table')


def start_filling(zte_type,nodes_tigger):

	cur_folder = Net_Folder(os.path.dirname(os.path.realpath('__file__')) + "/ZTE/" + zte_type)
	GSM = ZTE_Object(cur_folder)
	db = DataBasa(GSM,zte_type,nodes_tigger)
	db.result_to_sql()

