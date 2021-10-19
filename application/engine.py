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

def start_agg_to_csv(time_interval,claster_check,aggregation_time_type,aggregation_type):
	agg = Aggregation(time_interval,claster_check,aggregation_time_type,aggregation_type)
	agg.aggregate_to_csv()

def start_agg_to_dashboard_pickle(zte_type,time_interval,claster_check):
	cur_folder = Net_Folder(os.path.dirname(os.path.realpath('__file__')) + "/ZTE/" + zte_type)
	ZTE = ZTE_Object(cur_folder)	
	aggr = Aggregation(ZTE,zte_type,time_interval,claster_check)
	aggr.aggregate_to_dataframe()
