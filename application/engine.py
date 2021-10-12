from .unpacking_folders import *
from .metric_counters import *
from .databasa import *
from .agg import *


def start_filling(zte_type):
	cur_folder = Net_Folder(os.path.dirname(os.path.realpath('__file__')) + "/ZTE/" + zte_type)
	ZTE = ZTE_Object(cur_folder)
	db = DataBasa(ZTE,zte_type)
	db.result_to_pickle()
	# agg = Aggregation(GSM,zte_type)
	# agg.start_agg()

def start_agg(zte_type,time_interval,aggregation_time_type,aggregation_type):
	cur_folder = Net_Folder(os.path.dirname(os.path.realpath('__file__')) + "/ZTE/" + zte_type)
	ZTE = ZTE_Object(cur_folder)	
	agg = Aggregation(ZTE,zte_type,time_interval,aggregation_time_type,aggregation_type)
	agg.start_agg()
