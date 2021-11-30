from .unpacking_folders import *
from .metric_counters import *
from .databasa import *
from .agg import *

def start_filling(zte_type):
	cur_folder = Net_Folder(os.path.dirname(os.path.realpath('__file__')) + "/ZTE/" + zte_type) # Getting all static files for selected ZTE type
	ZTE = ZTE_Object(cur_folder) # Calculating counters, metrics and primary keys for selected ZTE type
	db = DataBasa(ZTE,zte_type) 
	db.result_to_pickle() # Creating pickle with attributes for selected ZTE type

def start_agg_to_csv(time_interval,claster_check,aggregation_time_type,aggregation_type):
	aggr = Aggregation(time_interval,claster_check,aggregation_time_type,aggregation_type) # setting form request values as arguments
	aggr.aggregate_to_csv()


