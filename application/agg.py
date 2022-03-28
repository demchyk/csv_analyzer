import pandas as pd
import numpy as np
import time
import datetime
import os
import shutil


class Aggregation:

    # Getting all needed info from dataframe attributes
    def __init__(self, date_range=None, claster_check=None, aggregation_time_type=None, aggregation_type=None):
        self.__df = self.__class__.__create_df_from_temp_pickle()
        self.__ZTE_type = self.__df.attrs['zte_type']
        self.__instructions_file = 'ZTE/' + self.__ZTE_type + '/requirements/' + 'formula.txt'
        self.__metrics = self.__class__.__metrics_from_file(self.__instructions_file)
        self.__metrics_names = list(self.__metrics.keys())
        self.__counters = self.__class__.__extract_counters_from_formulas(self.__instructions_file)
        self.__data_time_field_name = self.__df.attrs['data_time_field_name']
        self.__node_name = self.__df.attrs['node_name']
        self.__cell_name = self.__df.attrs['cell_name']
        self.__report_file_name = 'ZTE/' + self.__ZTE_type + '/reports/' + self.__ZTE_type
        self.__table_name = 'DB/' + self.__ZTE_type + '.pkl'
        self.__claster_check = claster_check
        self.__date_range = date_range
        self.__aggregation_time_type = aggregation_time_type
        self.__aggregation_type = aggregation_type
        self.__primary_keys = self.__df.attrs['primary_keys']

    # ----------------------------------------------------------------------------------
    @staticmethod
    def __create_df_from_temp_pickle():
        return pd.read_pickle('DB/export_to_csv.temp', compression='zip')

    # ----------------------------------------------------------------------------------
    @classmethod
    def __extract_counters_from_formulas(cls, instructions_file):
        formulas = cls.__extract_formulas_from_file(instructions_file)  # getting dict with formula name as key and expression as value
        all_counters = []
        for formula in formulas:
            expression = formula[formula.find('=') + 1 :]
            bad_words = '+-/*:.,()!@#$%^&'  # possible bad words in formula expression
            for word in bad_words:
                expression = expression.replace(word, ' ')  # getting rid of possible bad words
            text_list = [
                word.strip() for word in expression.split() if word[0].isalpha() and word[1:].isdigit()
            ]  # counter definiton is word with letter as first char and digits for the leftover
            all_counters += text_list
        return list(set(all_counters))  # list of counters without duplicates

    # ----------------------------------------------------------------------------------
    @staticmethod
    def __extract_formulas_from_file(instructions_file):
        with open(instructions_file, 'rt') as f:
            formulas = [formulas_temp.strip() for formulas_temp in f.readlines() if not formulas_temp.isspace()]  # checking for empty lines
        return formulas

    # ----------------------------------------------------------------------------------
    @classmethod
    def __agg_by_time(cls, df, primary_keys, data_time_field_name, frequency, metrics):
        if not frequency == 'H':  # to save time
            cutted_primary_keys = cls.__remover_collecttime_from_primary_keys(primary_keys, data_time_field_name)
            df = df.groupby([pd.Grouper(key=data_time_field_name, freq=frequency)] + cutted_primary_keys).sum()
            df.reset_index(inplace=True)
            return df
        return df

    # ----------------------------------------------------------------------------------
    @staticmethod
    def __remover_collecttime_from_primary_keys(primary_keys, data_time_field_name):
        copy_list = primary_keys[:]
        copy_list.remove(data_time_field_name)
        return copy_list

    # ----------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------
    # Calculate new dataframes columns (dict keys) as evaluated expressions (dict values)
    @classmethod
    def __swap_counters_for_metrics(cls, df, counters, instructions_file, metrics):
        df_columns = df.columns.tolist()
        primary_keys = [key for key in df_columns if key not in counters]
        for key, value in metrics.items():
            df[key] = np.around(df.eval(value), 2)
        final_table = df[primary_keys + list(metrics.keys())]
        return final_table

    # ----------------------------------------------------------------------------------
    # Splitting income data to start and end date as it comes in one variable
    @staticmethod
    def __agg_by_date_interval(df, date_range, data_time_field_name):
        date_start = date_range.split(' - ')[0]
        date_end = date_range.split(' - ')[1]
        df = df[(df[data_time_field_name] >= date_start) & (df[data_time_field_name] - datetime.timedelta(days=1) < date_end)]
        return df

    # ----------------------------------------------------------------------------------
    @classmethod
    def __agg_by_type(cls, df, aggregation_type, node_name, data_time_field_name, counters, primary_keys):
        if aggregation_type == 'CELL':
            df_fields = primary_keys + counters
            return df[df_fields]
        if aggregation_type == 'NODE':
            df_fields = [data_time_field_name, node_name] + counters  # getting rid of useless primary keys
            return df.groupby([data_time_field_name, node_name], as_index=False).sum()[df_fields]
        if aggregation_type == 'CLUSTER':
            claster_name, claster_values = cls.__get_claster_info(df)
            df_fields = [data_time_field_name, 'CLUSTER'] + counters  # getting rid of useless primary keys for the future
            df = (
                df[df[claster_name].astype(str).isin(claster_values)].groupby(data_time_field_name, as_index=False).sum()
            )  # converting to string because values from file come as integers
            df['CLUSTER'] = 'CLUSTER'  # new filed named CLUSTER with all values as CLUSTER
            return df[df_fields]

    # ----------------------------------------------------------------------------------
    @staticmethod
    def __get_claster_info(df):
        cluster_file = f'ZTE/{df.attrs["zte_type"]}/requirements/cluster.txt'
        with open(cluster_file, 'rt') as f:
            nodes = [nodes_temp.strip() for nodes_temp in f.readlines() if not nodes_temp.isspace()]  # check if line is empty
        return nodes[0], nodes[1:]  # claster field name as first parameter and values as second

    # ----------------------------------------------------------------------------------
    # If claster checkbox is selected - read info from cluster.txt and return it as 2d list (claster field name as first parameter and values as second)
    @classmethod
    def __apply_claster(cls, df, claster_check):
        if claster_check == 'cluster':
            claster_name, claster_values = cls.__get_claster_info(df)
            return df[df[claster_name].astype(str).isin(claster_values)]
        return df

    # ----------------------------------------------------------------------------------
    # Main function to get result from pickle to CSV
    def aggregate_to_csv(self):
        time1 = time.time()
        dframe = self.__agg_by_date_interval(self.__df, self.__date_range, self.__data_time_field_name)
        print(time.time() - time1)
        dframe = self.__apply_claster(dframe, self.__claster_check)
        print(time.time() - time1)
        dframe = self.__agg_by_time(dframe, self.__primary_keys, self.__data_time_field_name, self.__aggregation_time_type, self.__metrics)
        print(time.time() - time1)
        dframe = self.__agg_by_type(dframe, self.__aggregation_type, self.__node_name, self.__data_time_field_name, self.__counters, self.__primary_keys)
        print(time.time() - time1)
        dframe = self.__swap_counters_for_metrics(dframe, self.__counters, self.__instructions_file, self.__metrics)
        print(time.time() - time1)
        dframe.to_csv((f'{self.__report_file_name}-{self.__date_range}-{self.__aggregation_type}-{self.__aggregation_time_type}.csv').replace(' ', ''))

    # ----------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------
    # Get metrics from txt file
    @staticmethod
    def __metrics_from_file(instructions_file):
        with open(instructions_file, 'rt') as f:
            formulas = [formulas_temp.strip() for formulas_temp in f.readlines() if not formulas_temp.isspace()]  # checking for empty lines
        metrica_dic = {}
        for formula in formulas:
            metrica = formula[: formula.find('=')].strip()  # formula name (before first '=' )
            expression = formula[formula.find('=') + 1 :]  # formula expression (after first '=' )
            metrica_dic[metrica] = expression.strip()
        return metrica_dic


# ----------------------------------------------------------------------------------


# Out of class function to call it in __init__
def delete_temp_files(TEMP_FILES):
    for temp_file in TEMP_FILES:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    if os.path.exists('file_system_store'):
        shutil.rmtree('file_system_store', ignore_errors=True)


# ----------------------------------------------------------------------------------
