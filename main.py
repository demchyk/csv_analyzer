from unpacking_folders import *
from metric_counters import *
from databasa import *
from agg import *
import time


# cur_folder = Net_Folder(os.path.dirname(os.path.realpath('__file__')) + "/ZTE/LTE")
# GSM = ZTE_Object(cur_folder)
# db = DataBasa(GSM,'basa','table')


def start_filling(zte_type):
	cur_folder = Net_Folder(os.path.dirname(os.path.realpath('__file__')) + "/ZTE/" + zte_type)
	GSM = ZTE_Object(cur_folder)
	db = DataBasa(GSM,zte_type)
	db.result_to_pickle()
	# agg = Aggregation(GSM,zte_type)
	# agg.start_agg()

def start_agg(zte_type,time_interval,aggregation_time_type):
	cur_folder = Net_Folder(os.path.dirname(os.path.realpath('__file__')) + "/ZTE/" + zte_type)
	GSM = ZTE_Object(cur_folder)	
	agg = Aggregation(GSM,zte_type,time_interval,aggregation_time_type)
	agg.start_agg()
